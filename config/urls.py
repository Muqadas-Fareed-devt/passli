from django.contrib import admin
from django.urls import path, re_path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve

admin.site.site_header = "Passli Cryptographic Security Administration"
admin.site.site_title = "Passli Admin Portal"
admin.site.index_title = "System Management & Storage Console"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('accounts.urls')),
    path('documents/', include('documents.urls')),
    path('share/', include('sharing.urls')),
    path('p/', include('sharing.recipient_urls')),
    path('audit/', include('audit.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
else:
    # Production fallback media serving when object storage is not attached
    urlpatterns += [
        re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    ]
