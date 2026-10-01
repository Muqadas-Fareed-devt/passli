from django.contrib import admin
from django.utils.html import format_html
from .models import SharePass


@admin.register(SharePass)
class SharePassAdmin(admin.ModelAdmin):
    """
    Superadmin management for Ephemeral Share Passes.
    Provides live pass status badges, recipient usage monitoring, and bulk emergency revocation.
    """
    list_display = (
        'short_id',
        'title',
        'owner_link',
        'status_badge',
        'access_count_display',
        'can_download_badge',
        'expires_at',
        'created_at'
    )
    list_filter = ('is_revoked', 'can_download', 'created_at', 'expires_at')
    search_fields = ('id', 'title', 'owner__username', 'owner__email')
    readonly_fields = ('id', 'key_hash', 'access_count', 'created_at', 'updated_at')
    filter_horizontal = ('documents',)
    date_hierarchy = 'created_at'
    actions = ['emergency_revoke_passes']

    fieldsets = (
        ('Pass Identity & Owner', {
            'fields': ('id', 'owner', 'title', 'documents')
        }),
        ('Cryptographic Security & Constraints', {
            'fields': ('key_hash', 'expires_at', 'max_uses', 'access_count', 'can_download', 'is_revoked')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    @admin.display(description='Pass ID')
    def short_id(self, obj):
        return f"#{str(obj.id)[:8].upper()}"

    @admin.display(description='Owner', ordering='owner')
    def owner_link(self, obj):
        return f"{obj.owner.username} ({obj.owner.email})"

    @admin.display(description='Status')
    def status_badge(self, obj):
        if obj.is_revoked:
            return format_html('<span style="background: #ef4444; color: #fff; padding: 2px 8px; border-radius: 4px; font-size: 11px; font-weight: 700;">REVOKED</span>')
        elif obj.is_expired():
            return format_html('<span style="background: #f59e0b; color: #fff; padding: 2px 8px; border-radius: 4px; font-size: 11px; font-weight: 700;">EXPIRED</span>')
        return format_html('<span style="background: #10b981; color: #fff; padding: 2px 8px; border-radius: 4px; font-size: 11px; font-weight: 700;">ACTIVE</span>')

    @admin.display(description='Accesses / Limit')
    def access_count_display(self, obj):
        limit = f" / {obj.max_uses}" if obj.max_uses > 0 else " (unlimited)"
        return f"{obj.access_count}{limit}"

    @admin.display(description='Download Permitted')
    def can_download_badge(self, obj):
        if obj.can_download:
            return format_html('<span style="color: #10b981; font-weight: 700;">✓ Allowed</span>')
        return format_html('<span style="color: #6b7280;">✕ View Only</span>')

    @admin.action(description='⚡ Emergency Revoke selected Share Passes')
    def emergency_revoke_passes(self, request, queryset):
        updated = queryset.update(is_revoked=True)
        self.message_user(request, f"{updated} Share Pass(es) successfully revoked.")

