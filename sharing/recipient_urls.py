from django.urls import path
from . import recipient_views

urlpatterns = [
    path('<uuid:pass_id>/', recipient_views.recipient_verify_view, name='recipient_verify'),
    path('<uuid:pass_id>/portal/', recipient_views.recipient_portal_view, name='recipient_portal'),
    path('<uuid:pass_id>/doc/<int:doc_id>/preview/', recipient_views.recipient_doc_preview_view, name='recipient_doc_preview'),
    path('<uuid:pass_id>/doc/<int:doc_id>/download/', recipient_views.recipient_doc_download_view, name='recipient_doc_download'),
    path('<uuid:pass_id>/leave/', recipient_views.recipient_leave_view, name='recipient_leave'),
]
