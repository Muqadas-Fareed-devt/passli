from django.urls import path
from . import views

urlpatterns = [
    path('', views.documents_list_view, name='documents_list'),
    path('upload/', views.documents_upload_view, name='documents_upload'),
    path('upload/', views.documents_upload_view, name='document_upload'),
    path('<int:pk>/', views.document_detail_view, name='document_detail'),
    path('<int:pk>/preview/', views.document_preview_view, name='document_preview'),
    path('<int:pk>/download/', views.document_download_view, name='document_download'),
    path('<int:pk>/edit/', views.document_edit_view, name='document_edit'),
    path('<int:pk>/delete/', views.document_delete_view, name='document_delete'),
]
