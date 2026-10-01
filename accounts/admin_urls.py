from django.urls import path
from . import admin_views

urlpatterns = [
    path('', admin_views.admin_dashboard_overview, name='admin_dashboard_overview'),
    path('users/', admin_views.admin_dashboard_users, name='admin_dashboard_users'),
    path('users/<int:user_id>/toggle-status/', admin_views.admin_user_toggle_status, name='admin_user_toggle_status'),
    path('documents/', admin_views.admin_dashboard_documents, name='admin_dashboard_documents'),
    path('documents/<int:doc_id>/delete/', admin_views.admin_document_delete, name='admin_document_delete'),
    path('passes/', admin_views.admin_dashboard_passes, name='admin_dashboard_passes'),
    path('passes/<uuid:pass_id>/revoke/', admin_views.admin_pass_revoke, name='admin_pass_revoke'),
    path('audit/', admin_views.admin_dashboard_audit, name='admin_dashboard_audit'),
]
