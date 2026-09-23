import os
import uuid
import hashlib
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


def document_upload_path(instance, filename):
    """
    Generates a secure, sanitized, user-isolated file path.
    Always uses POSIX forward slashes for cross-platform compatibility (Windows & Linux/Railway).
    Format: vault_files/user_<id>/<uuid>.<ext>
    """
    ext = os.path.splitext(filename)[1].lower()
    unique_name = f"{uuid.uuid4().hex}{ext}"
    user_id = instance.user_id if instance.user_id else 'anon'
    return f"vault_files/user_{user_id}/{unique_name}"


class Document(models.Model):
    """
    Encrypted Personal Vault Document record.
    Stores metadata, domain classification, MIME type, file size, and SHA-256 integrity checksum.
    """

    CATEGORY_CHOICES = [
        ('medical', 'Medical Records'),
        ('education', 'Education & Degrees'),
        ('vehicle', 'Vehicle & Asset'),
        ('personal', 'Personal & Identity'),
        ('professional', 'Professional & Employment'),
        ('other', 'Other Records'),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='documents',
        verbose_name='Vault Owner'
    )
    title = models.CharField(
        max_length=255,
        verbose_name='Document Title'
    )
    category = models.CharField(
        max_length=50,
        choices=CATEGORY_CHOICES,
        default='other',
        verbose_name='Category Domain'
    )
    description = models.TextField(
        blank=True,
        verbose_name='Description / Notes'
    )
    file = models.FileField(
        upload_to=document_upload_path,
        verbose_name='Vault File'
    )
    original_filename = models.CharField(
        max_length=255,
        blank=True,
        verbose_name='Original Filename'
    )
    file_type = models.CharField(
        max_length=100,
        blank=True,
        verbose_name='MIME / Content Type'
    )
    file_size = models.BigIntegerField(
        default=0,
        verbose_name='File Size (Bytes)'
    )
    file_hash = models.CharField(
        max_length=64,
        blank=True,
        verbose_name='SHA-256 Checksum'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Created At'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Updated At'
    )

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', 'category']),
            models.Index(fields=['user', 'created_at']),
        ]
        verbose_name = 'Vault Document'
        verbose_name_plural = 'Vault Documents'

    def __str__(self):
        return f"{self.title} ({self.get_category_display()})"

    def save(self, *args, **kwargs):
        """Compute SHA-256 checksum and record size safely before saving."""
        if self.file and hasattr(self.file, 'name'):
            # Record original filename if not already set
            if not self.original_filename:
                self.original_filename = os.path.basename(self.file.name)

            # Detect content type from extension if empty
            if not self.file_type and self.original_filename:
                ext = os.path.splitext(self.original_filename)[1].lower()
                mime_map = {
                    '.pdf': 'application/pdf',
                    '.png': 'image/png',
                    '.jpg': 'image/jpeg',
                    '.jpeg': 'image/jpeg',
                }
                self.file_type = mime_map.get(ext, 'application/octet-stream')

            # Calculate SHA-256 digest safely using chunks()
            if not self.file_hash:
                hasher = hashlib.sha256()
                size = 0
                try:
                    if hasattr(self.file, 'chunks'):
                        for chunk in self.file.chunks():
                            hasher.update(chunk)
                            size += len(chunk)
                        self.file_hash = hasher.hexdigest()
                        self.file_size = size or getattr(self.file, 'size', 0)
                    elif hasattr(self.file, 'file'):
                        self.file.seek(0)
                        for chunk in iter(lambda: self.file.read(65536), b''):
                            hasher.update(chunk)
                            size += len(chunk)
                        self.file_hash = hasher.hexdigest()
                        self.file_size = size or getattr(self.file, 'size', 0)
                        self.file.seek(0)
                except Exception:
                    pass

        super().save(*args, **kwargs)

    @property
    def formatted_size(self):
        """Human-readable file size string (e.g. 2.4 MB, 450 KB)."""
        if not self.file_size:
            return "0 KB"
        size = float(self.file_size)
        if size < 1024:
            return f"{size:.0f} B"
        elif size < 1024 * 1024:
            return f"{size / 1024:.1f} KB"
        else:
            return f"{size / (1024 * 1024):.1f} MB"

    @property
    def is_pdf(self):
        """Check if document is a PDF format safely."""
        if not self.file:
            return False
        file_type_pdf = bool(self.file_type and self.file_type.lower() == 'application/pdf')
        file_name_pdf = bool(getattr(self.file, 'name', None) and str(self.file.name).lower().endswith('.pdf'))
        return file_type_pdf or file_name_pdf

    @property
    def is_image(self):
        """Check if document is an image format safely."""
        if not self.file:
            return False
        file_type_img = bool(self.file_type and self.file_type.lower().startswith('image/'))
        file_name_img = bool(getattr(self.file, 'name', None) and str(self.file.name).lower().endswith(('.png', '.jpg', '.jpeg', '.webp')))
        return file_type_img or file_name_img

    @property
    def category_icon(self):
        """Material symbol icon for the domain."""
        icon_map = {
            'medical': 'medical_services',
            'education': 'school',
            'vehicle': 'directions_car',
            'personal': 'badge',
            'professional': 'work',
            'other': 'description',
        }
        return icon_map.get(self.category, 'description')

