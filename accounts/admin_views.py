import os
import logging
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import user_passes_test
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Sum, Count, Q
from django.utils import timezone

from documents.models import Document
from sharing.models import SharePass
from audit.models import ShareAccessLog, log_share_event

logger = logging.getLogger(__name__)
User = get_user_model()


def superadmin_required(view_func):
    """Decorator ensuring only staff members or superusers can access the administration console."""
    actual_decorator = user_passes_test(
        lambda u: u.is_authenticated and (u.is_staff or u.is_superuser),
        login_url='login'
    )
    return actual_decorator(view_func)


@superadmin_required
def admin_dashboard_overview(request):
    """
    Main Administration Console Dashboard.
    Provides system-wide telemetry, storage quota breakdown, user metrics, and quick admin controls.
    """
    # 1. User metrics
    total_users = User.objects.count()
    active_users = User.objects.filter(is_active=True).count()
    staff_users = User.objects.filter(is_staff=True).count()

    # 2. Document & Storage metrics
    total_docs = Document.objects.count()
    storage_agg = Document.objects.aggregate(total_bytes=Sum('file_size'))
    total_bytes = storage_agg['total_bytes'] or 0
    total_mb = total_bytes / (1024 * 1024)
    total_gb = total_mb / 1024

    # Storage by category
    categories = ['medical', 'education', 'vehicle', 'personal', 'professional', 'other']
    category_stats = []
    for cat in categories:
        cat_docs = Document.objects.filter(category=cat)
        cat_count = cat_docs.count()
        cat_bytes = cat_docs.aggregate(total=Sum('file_size'))['total'] or 0
        cat_mb = cat_bytes / (1024 * 1024)
        percentage = (cat_bytes / total_bytes * 100) if total_bytes > 0 else 0
        category_stats.append({
            'code': cat,
            'label': dict(Document.CATEGORY_CHOICES).get(cat, cat.title()),
            'count': cat_count,
            'mb': f"{cat_mb:.2f}",
            'percentage': f"{percentage:.1f}",
        })

    # 3. Share Pass metrics
    now = timezone.now()
    total_passes = SharePass.objects.count()
    active_passes = SharePass.objects.filter(is_revoked=False, expires_at__gt=now).count()
    revoked_passes = SharePass.objects.filter(is_revoked=True).count()
    expired_passes = SharePass.objects.filter(is_revoked=False, expires_at__lte=now).count()

    # 4. Security & Audit metrics
    total_audit_events = ShareAccessLog.objects.count()
    total_unlocks = ShareAccessLog.objects.filter(event_type=ShareAccessLog.EventType.KEY_SUCCESS).count()
    blocked_threats = ShareAccessLog.objects.filter(
        event_type__in=[
            ShareAccessLog.EventType.KEY_FAILED,
            ShareAccessLog.EventType.RATE_LOCKED,
            ShareAccessLog.EventType.PASS_REVOKED,
            ShareAccessLog.EventType.PASS_EXPIRED,
        ]
    ).count()

    # 5. Recent Activity Stream
    recent_users = User.objects.order_by('-date_joined')[:5]
    recent_passes = SharePass.objects.select_related('owner').order_by('-created_at')[:5]
    recent_audit_logs = ShareAccessLog.objects.select_related('share_pass', 'document').order_by('-timestamp')[:6]

    context = {
        'total_users': total_users,
        'active_users': active_users,
        'staff_users': staff_users,
        'total_docs': total_docs,
        'total_mb': f"{total_mb:.2f}",
        'total_gb': f"{total_gb:.3f}",
        'total_bytes': total_bytes,
        'category_stats': category_stats,
        'total_passes': total_passes,
        'active_passes': active_passes,
        'revoked_passes': revoked_passes,
        'expired_passes': expired_passes,
        'total_audit_events': total_audit_events,
        'total_unlocks': total_unlocks,
        'blocked_threats': blocked_threats,
        'recent_users': recent_users,
        'recent_passes': recent_passes,
        'recent_audit_logs': recent_audit_logs,
        'active_tab': 'overview',
    }
    return render(request, 'administration/overview.html', context)


@superadmin_required
def admin_dashboard_users(request):
    """
    User Management Console.
    Lists all registered users with their vault document counts, storage quota consumption, and staff roles.
    """
    query = request.GET.get('q', '').strip()
    status_filter = request.GET.get('status', '')

    users_qs = User.objects.annotate(
        docs_count=Count('documents', distinct=True),
        total_bytes=Sum('documents__file_size'),
        passes_count=Count('share_passes', distinct=True)
    ).order_by('-date_joined')

    if query:
        users_qs = users_qs.filter(
            Q(username__icontains=query) |
            Q(email__icontains=query) |
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query)
        )

    if status_filter == 'staff':
        users_qs = users_qs.filter(is_staff=True)
    elif status_filter == 'active':
        users_qs = users_qs.filter(is_active=True)
    elif status_filter == 'inactive':
        users_qs = users_qs.filter(is_active=False)

    paginator = Paginator(users_qs, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Attach formatted MB property
    for user in page_obj.object_list:
        b = user.total_bytes or 0
        user.storage_mb = f"{(b / (1024 * 1024)):.2f}"

    context = {
        'page_obj': page_obj,
        'users': page_obj.object_list,
        'query': query,
        'status_filter': status_filter,
        'total_count': users_qs.count(),
        'active_tab': 'users',
    }
    return render(request, 'administration/users.html', context)


@superadmin_required
@require_POST
def admin_user_toggle_status(request, user_id):
    """Allows superadmins to toggle active status or staff role of a user."""
    target_user = get_object_or_404(User, id=user_id)
    action_type = request.POST.get('action_type')

    # Prevent deactivating or un-staffing oneself
    if target_user.id == request.user.id:
        messages.error(request, "You cannot modify your own administrative status.")
        return redirect('admin_dashboard_users')

    if action_type == 'toggle_active':
        target_user.is_active = not target_user.is_active
        target_user.save(update_fields=['is_active'])
        status_label = "activated" if target_user.is_active else "deactivated"
        messages.success(request, f"User '{target_user.username}' successfully {status_label}.")
    elif action_type == 'toggle_staff':
        target_user.is_staff = not target_user.is_staff
        target_user.save(update_fields=['is_staff'])
        role_label = "granted staff access" if target_user.is_staff else "revoked from staff"
        messages.success(request, f"User '{target_user.username}' {role_label}.")

    return redirect('admin_dashboard_users')


@superadmin_required
def admin_dashboard_documents(request):
    """
    Platform-Wide Storage & Document Vault Console.
    Inspects all ingested documents, sizes, categories, and cryptographic SHA-256 digests.
    """
    query = request.GET.get('q', '').strip()
    category_filter = request.GET.get('category', '')
    owner_query = request.GET.get('owner', '').strip()

    docs_qs = Document.objects.select_related('user').order_by('-created_at')

    if query:
        docs_qs = docs_qs.filter(
            Q(title__icontains=query) |
            Q(original_filename__icontains=query) |
            Q(file_hash__icontains=query)
        )

    if category_filter:
        docs_qs = docs_qs.filter(category=category_filter)

    if owner_query:
        docs_qs = docs_qs.filter(user__username__icontains=owner_query)

    total_size_bytes = docs_qs.aggregate(total=Sum('file_size'))['total'] or 0
    total_size_mb = total_size_bytes / (1024 * 1024)

    paginator = Paginator(docs_qs, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'documents': page_obj.object_list,
        'query': query,
        'category_filter': category_filter,
        'owner_query': owner_query,
        'total_count': docs_qs.count(),
        'total_size_mb': f"{total_size_mb:.2f}",
        'category_choices': Document.CATEGORY_CHOICES,
        'active_tab': 'documents',
    }
    return render(request, 'administration/documents.html', context)


@superadmin_required
@require_POST
def admin_document_delete(request, doc_id):
    """Allows superadmins to delete a vault document with physical storage file cleanup."""
    doc = get_object_or_404(Document, id=doc_id)
    title = doc.title
    owner_name = doc.user.username

    # Remove physical file
    if doc.file and os.path.exists(doc.file.path):
        try:
            os.remove(doc.file.path)
        except OSError as e:
            logger.error(f"Error removing physical document file: {e}")

    doc.delete()
    messages.success(request, f"Document '{title}' belonging to user '{owner_name}' permanently deleted.")
    return redirect('admin_dashboard_documents')


@superadmin_required
def admin_dashboard_passes(request):
    """
    Share Pass Administration Console.
    Monitors all active, expired, and revoked passes, usage limits, and enables 1-click emergency revocation.
    """
    query = request.GET.get('q', '').strip()
    status_filter = request.GET.get('status', '')

    now = timezone.now()
    passes_qs = SharePass.objects.select_related('owner').prefetch_related('documents').order_by('-created_at')

    if query:
        passes_qs = passes_qs.filter(
            Q(title__icontains=query) |
            Q(id__icontains=query) |
            Q(owner__username__icontains=query) |
            Q(owner__email__icontains=query)
        )

    if status_filter == 'active':
        passes_qs = passes_qs.filter(is_revoked=False, expires_at__gt=now)
    elif status_filter == 'revoked':
        passes_qs = passes_qs.filter(is_revoked=True)
    elif status_filter == 'expired':
        passes_qs = passes_qs.filter(is_revoked=False, expires_at__lte=now)

    paginator = Paginator(passes_qs, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'share_passes': page_obj.object_list,
        'query': query,
        'status_filter': status_filter,
        'total_count': passes_qs.count(),
        'active_tab': 'passes',
    }
    return render(request, 'administration/passes.html', context)


@superadmin_required
@require_POST
def admin_pass_revoke(request, pass_id):
    """Emergency revocation of any Share Pass by superadministrator."""
    share_pass = get_object_or_404(SharePass, id=pass_id)
    share_pass.is_revoked = True
    share_pass.save(update_fields=['is_revoked', 'updated_at'])

    # Structured audit logging for admin revocation
    log_share_event(
        share_pass=share_pass,
        event_type=ShareAccessLog.EventType.PASS_REVOKED,
        request=request,
        status=ShareAccessLog.Status.REVOKED,
        details=f"Emergency revocation by Superadmin @{request.user.username}"
    )

    messages.success(request, f"Share Pass #{str(share_pass.id)[:8].upper()} ('{share_pass.title or 'Untitled'}') immediately revoked.")
    return redirect('admin_dashboard_passes')


@superadmin_required
def admin_dashboard_audit(request):
    """
    Global Security Threat & Audit Trail Console.
    Inspects all system-wide access attempts, brute-force lockouts, and verification outcomes.
    """
    query = request.GET.get('q', '').strip()
    event_filter = request.GET.get('event', '')
    status_filter = request.GET.get('status', '')

    logs_qs = ShareAccessLog.objects.select_related('share_pass', 'share_pass__owner', 'document').order_by('-timestamp')

    if query:
        logs_qs = logs_qs.filter(
            Q(ip_address__icontains=query) |
            Q(user_agent__icontains=query) |
            Q(details__icontains=query) |
            Q(share_pass__title__icontains=query) |
            Q(share_pass__owner__username__icontains=query)
        )

    if event_filter:
        logs_qs = logs_qs.filter(event_type=event_filter)

    if status_filter:
        logs_qs = logs_qs.filter(status=status_filter)

    paginator = Paginator(logs_qs, 25)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'logs': page_obj.object_list,
        'query': query,
        'event_filter': event_filter,
        'status_filter': status_filter,
        'total_count': logs_qs.count(),
        'event_choices': ShareAccessLog.EventType.choices,
        'status_choices': ShareAccessLog.Status.choices,
        'active_tab': 'audit',
    }
    return render(request, 'administration/audit.html', context)
