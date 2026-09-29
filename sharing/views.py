from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.http import FileResponse, Http404
from django.urls import reverse

from documents.models import Document
from .models import SharePass
from .forms import SharePassCreateForm
from .utils import generate_share_key, generate_qr_data_uri, generate_qr_image_buffer


@login_required
def share_create_view(request):
    """
    Creates a new time-gated, cryptographic Share Pass.
    Generates a secure 8-character Share Key, stores only its PBKDF2 hash,
    and returns the one-time raw key for the owner to record or hand off.
    """
    user_docs_count = Document.objects.filter(user=request.user).count()

    if request.method == 'POST':
        form = SharePassCreateForm(request.POST, user=request.user)
        if form.is_valid():
            share_pass = form.save(commit=False)
            share_pass.owner = request.user

            # Generate and hash ephemeral cryptographic Share Key
            raw_key = generate_share_key()
            share_pass.set_key(raw_key)

            # Compute expiration timestamp & usage limit
            expires_at, max_uses = form.get_expiration_and_max_uses()
            share_pass.expires_at = expires_at
            share_pass.max_uses = max_uses
            share_pass.save()

            # Save attached documents (many-to-many)
            form.save_m2m()

            # Store plaintext key in session for one-time display on detail page
            request.session[f'new_pass_key_{share_pass.id}'] = raw_key

            messages.success(
                request,
                f"Share Pass '{share_pass.title or str(share_pass.id)[:8]}' created! Ensure you share the access key with the recipient."
            )
            return redirect('share_detail', pass_id=share_pass.id)
    else:
        # Pre-select document if doc_id passed via query param (e.g. from document list)
        initial_data = {}
        preselected_doc_id = request.GET.get('doc')
        if preselected_doc_id:
            try:
                doc = Document.objects.get(id=preselected_doc_id, user=request.user)
                initial_data['documents'] = [doc.id]
            except (Document.DoesNotExist, ValueError):
                pass

        form = SharePassCreateForm(user=request.user, initial=initial_data)

    context = {
        'form': form,
        'user_docs_count': user_docs_count,
        'active_page': 'share_create',
    }
    return render(request, 'sharing/create.html', context)


@login_required
def share_detail_view(request, pass_id):
    """
    Displays the Share Pass management view, dynamic QR code,
    one-time Share Key (if newly created), attached records, and live status.
    Enforces strict IDOR object ownership checks.
    """
    share_pass = get_object_or_404(
        SharePass.objects.prefetch_related('documents'),
        id=pass_id,
        owner=request.user
    )

    # Retrieve one-time raw key if just created in this session
    session_key = f'new_pass_key_{share_pass.id}'
    raw_key = request.session.get(session_key, None)

    # Generate QR Code Data URI targeting public recipient endpoint
    recipient_url = share_pass.get_recipient_url(request)
    qr_data_uri = generate_qr_data_uri(recipient_url)

    context = {
        'pass': share_pass,
        'raw_key': raw_key,
        'recipient_url': recipient_url,
        'qr_data_uri': qr_data_uri,
        'documents': share_pass.documents.all(),
        'active_page': 'share_passes',
    }
    return render(request, 'sharing/detail.html', context)


@login_required
def share_list_view(request):
    """
    Lists all active, expired, and revoked Share Passes created by the current user.
    """
    passes = SharePass.objects.filter(owner=request.user).prefetch_related('documents').order_by('-created_at')

    # Summary metrics
    total_passes = passes.count()
    active_passes = [p for p in passes if p.is_active()]
    expired_passes = [p for p in passes if p.is_expired() and not p.is_revoked]
    revoked_passes = [p for p in passes if p.is_revoked]

    context = {
        'passes': passes,
        'total_count': total_passes,
        'active_count': len(active_passes),
        'expired_count': len(expired_passes),
        'revoked_count': len(revoked_passes),
        'active_page': 'share_passes',
    }
    return render(request, 'sharing/list.html', context)


@login_required
@require_POST
def share_revoke_view(request, pass_id):
    """
    Immediately revokes a Share Pass, terminating all recipient access.
    Enforces strict IDOR check and CSRF token.
    """
    share_pass = get_object_or_404(SharePass, id=pass_id, owner=request.user)
    share_pass.revoke()

    from audit.models import ShareAccessLog, log_share_event
    log_share_event(
        share_pass,
        ShareAccessLog.EventType.PASS_REVOKED,
        request=request,
        status=ShareAccessLog.Status.REVOKED,
        details=f"Revoked by owner ({request.user.username})"
    )

    messages.warning(
        request,
        f"Share Pass '{share_pass.title or str(share_pass.id)[:8]}' was immediately revoked. Access is blocked."
    )

    # Redirect to list or detail
    redirect_target = request.POST.get('next', reverse('share_detail', kwargs={'pass_id': share_pass.id}))
    return redirect(redirect_target)


@login_required
def share_qr_download_view(request, pass_id):
    """
    Streams the high-resolution QR Code PNG as a downloadable attachment.
    """
    share_pass = get_object_or_404(SharePass, id=pass_id, owner=request.user)
    recipient_url = share_pass.get_recipient_url(request)
    qr_buffer = generate_qr_image_buffer(recipient_url)

    filename = f"passli-qr-{str(share_pass.id)[:8]}.png"
    response = FileResponse(qr_buffer, content_type='image/png')
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    return response
