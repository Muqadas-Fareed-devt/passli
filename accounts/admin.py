from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.db.models import Sum, Count
from django.utils.html import format_html

User = get_user_model()

# Unregister default UserAdmin
admin.site.unregister(User)


@admin.register(User)
class CustomUserAdmin(BaseUserAdmin):
    """
    Superadmin user manager enhanced with Passli Vault storage metrics,
    document counts, and active Share Pass indicators.
    """
    list_display = (
        'username',
        'email',
        'vault_docs_count',
        'vault_storage_used',
        'active_passes_count',
        'is_staff',
        'date_joined'
    )
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'date_joined')
    search_fields = ('username', 'email', 'first_name', 'last_name')

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.annotate(
            docs_count=Count('documents', distinct=True),
            total_bytes=Sum('documents__file_size'),
            passes_count=Count('share_passes', distinct=True)
        )

    @admin.display(description='Vault Records', ordering='docs_count')
    def vault_docs_count(self, obj):
        count = getattr(obj, 'docs_count', 0)
        return format_html('<strong>{}</strong> doc(s)', count)

    @admin.display(description='Storage Quota Used', ordering='total_bytes')
    def vault_storage_used(self, obj):
        total_bytes = getattr(obj, 'total_bytes', 0) or 0
        mb = total_bytes / (1024 * 1024)
        if mb >= 1024:
            return f"{mb / 1024:.2f} GB"
        elif mb > 0:
            return f"{mb:.2f} MB"
        elif total_bytes > 0:
            return f"{total_bytes / 1024:.1f} KB"
        return "0 KB"

    @admin.display(description='Share Passes', ordering='passes_count')
    def active_passes_count(self, obj):
        count = getattr(obj, 'passes_count', 0)
        return format_html('<span style="color: #6366f1; font-weight: 600;">{} pass(es)</span>', count)

