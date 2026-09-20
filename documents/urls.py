from django.urls import path
from . import views

urlpatterns = [
    path('', views.documents_list_view, name='documents_list'),
    path('upload/', views.documents_upload_view, name='documents_upload'),
]
