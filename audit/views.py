import logging
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from .models import ShareAccessLog
from sharing.models import SharePass

logger = logging.getLogger(__name__)


@login_required
def audit_list_view(request):
    """
    Owner access log dashboard.
    Renders chronological structured audit trail of all access events, verification
    attempts, file downloads, and security interventions across the owner's share passes.
    Enforces strict IDOR isolation: users only see audit events for passes they own.
    """
    # Base queryset restricted to owner's share passes
    logs = ShareAccessLog.objects.filter(
        share_pass__owner=request.user
    ).select_related('share_pass', 'document').order_by('-timestamp')

    # Get list of owner's passes for filter dropdown
    owner_passes = SharePass.objects.filter(owner=request.user).order_by('-created_at')

    # Filter by specific pass
    selected_pass_id = request.GET.get('pass')
    if selected_pass_id:
        logs = logs.filter(share_pass_id=selected_pass_id)

    # Filter by event type
    selected_event = request.GET.get('event')
    if selected_event:
        logs = logs.filter(event_type=selected_event)

    # Filter by status
    selected_status = request.GET.get('status')
    if selected_status:
        logs = logs.filter(status=selected_status)

    # Search keyword
    query = request.GET.get('q', '').strip()
    if query:
        logs = logs.filter(
            Q(details__icontains=query) |
            Q(ip_address__icontains=query) |
            Q(share_pass__title__icontains=query) |
            Q(document__title__icontains=query)
        )

    # Calculate overall security metrics for owner
    all_owner_logs = ShareAccessLog.objects.filter(share_pass__owner=request.user)
    total_events = all_owner_logs.count()
    successful_unlocks = all_owner_logs.filter(event_type=ShareAccessLog.EventType.KEY_SUCCESS).count()
    blocked_attempts = all_owner_logs.filter(
        event_type__in=[
            ShareAccessLog.EventType.KEY_FAILED,
            ShareAccessLog.EventType.RATE_LOCKED,
            ShareAccessLog.EventType.PASS_EXPIRED,
            ShareAccessLog.EventType.PASS_REVOKED
        ]
    ).count()
    downloads_count = all_owner_logs.filter(event_type=ShareAccessLog.EventType.DOWNLOAD_DOC).count()

    # Pagination
    paginator = Paginator(logs, 25)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'logs': page_obj.object_list,
        'owner_passes': owner_passes,
        'total_events': total_events,
        'successful_unlocks': successful_unlocks,
        'blocked_attempts': blocked_attempts,
        'downloads_count': downloads_count,
        'selected_pass_id': selected_pass_id or '',
        'selected_event': selected_event or '',
        'selected_status': selected_status or '',
        'query': query,
        'event_choices': ShareAccessLog.EventType.choices,
        'status_choices': ShareAccessLog.Status.choices,
        'active_page': 'audit',
    }
    return render(request, 'audit/list.html', context)
