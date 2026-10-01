from django.contrib import admin
from django.utils.html import format_html
from .models import Document


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    """
    Superadmin management for Encrypted Document Vault records.
    Provides storage metrics, MIME inspection, SHA-256 integrity checks, and user isolation filters.
    """
    list_display = (
        'title',
        'user_link',
        'category_badge',
        'formatted_file_size',
        'file_type',
        'checksum_short',
        'created_at'
    )
    list_filter = ('category', 'created_at', 'file_type')
    search_fields = ('title', 'original_filename', 'file_hash', 'user__username', 'user__email')
    readonly_fields = ('file_hash', 'file_size', 'file_type', 'original_filename', 'created_at', 'updated_at')
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)

    fieldsets = (
        ('Document Details', {
            'fields': ('user', 'title', 'category', 'description', 'file')
        }),
        ('Cryptographic Integrity & Metadata', {
            'fields': ('original_filename', 'file_type', 'file_size', 'file_hash'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    @admin.display(description='Vault Owner', ordering='user')
    def user_link(self, obj):
        return f"{obj.user.username} ({obj.user.email})"

    @admin.display(description='Category')
    def category_badge(self, obj):
        colors = {
            'medical': '#10b981',
            'education': '#3b82f6',
            'vehicle': '#f59e0b',
            'personal': '#8b5cf6',
            'professional': '#06b6d4',
            'other': '#6b7280',
        }
        color = colors.get(obj.category, '#6b7280')
        return format_html(
            '<span style="background: {}; color: #fff; padding: 2px 8px; border-radius: 4px; font-size: 11px; font-weight: 600;">{}</span>',
            color,
            obj.get_category_display()
        )

    @admin.display(description='Size', ordering='file_size')
    def formatted_file_size(self, obj):
        return obj.formatted_size

    @admin.display(description='SHA-256 Checksum')
    def checksum_short(self, obj):
        if obj.file_hash:
            return format_html(
                '<code style="font-size: 11px; background: #f1f5f9; padding: 2px 6px; border-radius: 3px;" title="{}">{}…</code>',
                obj.file_hash,
                obj.file_hash[:12]
            )
        return "-"

