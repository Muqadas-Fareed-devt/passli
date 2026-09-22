from django.urls import path
from . import views

urlpatterns = [
    path('', views.share_list_view, name='share_list'),
    path('create/', views.share_create_view, name='share_create'),
    path('<uuid:pass_id>/', views.share_detail_view, name='share_detail'),
    path('<uuid:pass_id>/revoke/', views.share_revoke_view, name='share_revoke'),
    path('<uuid:pass_id>/qr/download/', views.share_qr_download_view, name='share_qr_download'),
]
