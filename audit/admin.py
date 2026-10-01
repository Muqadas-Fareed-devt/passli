from django.contrib import admin
from django.utils.html import format_html
from .models import ShareAccessLog


@admin.register(ShareAccessLog)
class ShareAccessLogAdmin(admin.ModelAdmin):
    """
    Superadmin security audit trail console.
    Provides threat detection, brute-force lockout monitoring, IP address tracking, and event logs.
    """
    list_display = (
        'timestamp',
        'event_badge',
        'status_badge',
        'pass_link',
        'document_link',
        'ip_address',
        'user_agent_short',
        'details'
    )
    list_filter = ('event_type', 'status', 'timestamp')
    search_fields = (
        'ip_address',
        'user_agent',
        'details',
        'share_pass__title',
        'share_pass__owner__username',
        'document__title'
    )
    readonly_fields = (
        'share_pass',
        'document',
        'timestamp',
        'event_type',
        'status',
        'ip_address',
        'user_agent',
        'details'
    )
    date_hierarchy = 'timestamp'
    ordering = ('-timestamp',)

    def has_add_permission(self, request):
        # Audit logs are immutable records created only via system triggers
        return False

    def has_change_permission(self, request, obj=None):
        # Prevent manual tampering with audit entries
        return False

    @admin.display(description='Event Type', ordering='event_type')
    def event_badge(self, obj):
        colors = {
            ShareAccessLog.EventType.KEY_SUCCESS: '#10b981',
            ShareAccessLog.EventType.KEY_FAILED: '#f43f5e',
            ShareAccessLog.EventType.RATE_LOCKED: '#dc2626',
            ShareAccessLog.EventType.VIEW_PORTAL: '#3b82f6',
            ShareAccessLog.EventType.VIEW_DOC: '#06b6d4',
            ShareAccessLog.EventType.DOWNLOAD_DOC: '#6366f1',
            ShareAccessLog.EventType.SESSION_LEFT: '#64748b',
            ShareAccessLog.EventType.PASS_REVOKED: '#991b1b',
            ShareAccessLog.EventType.PASS_EXPIRED: '#d97706',
        }
        color = colors.get(obj.event_type, '#6b7280')
        return format_html(
            '<span style="background: {}; color: #fff; padding: 2px 8px; border-radius: 4px; font-size: 11px; font-weight: 600;">{}</span>',
            color,
            obj.get_event_type_display()
        )

    @admin.display(description='Status')
    def status_badge(self, obj):
        status_colors = {
            ShareAccessLog.Status.SUCCESS: '#10b981',
            ShareAccessLog.Status.DENIED: '#f43f5e',
            ShareAccessLog.Status.LOCKED: '#dc2626',
            ShareAccessLog.Status.EXPIRED: '#d97706',
            ShareAccessLog.Status.REVOKED: '#991b1b',
        }
        color = status_colors.get(obj.status, '#6b7280')
        return format_html(
            '<span style="color: {}; font-weight: 700; font-size: 11px;">{}</span>',
            color,
            obj.status.upper()
        )

    @admin.display(description='Share Pass')
    def pass_link(self, obj):
        if obj.share_pass:
            title = obj.share_pass.title or f"Pass #{str(obj.share_pass.id)[:8]}"
            owner = obj.share_pass.owner.username if obj.share_pass.owner else "Unknown"
            return f"{title} (Owner: {owner})"
        return "-"

    @admin.display(description='Document')
    def document_link(self, obj):
        if obj.document:
            return obj.document.title
        return format_html('<span style="color: #94a3b8; font-style: italic;">Envelope Root</span>')

    @admin.display(description='User Agent')
    def user_agent_short(self, obj):
        if obj.user_agent:
            return obj.user_agent[:45] + ('…' if len(obj.user_agent) > 45 else '')
        return "-"

