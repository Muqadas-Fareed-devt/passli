from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.share_create_view, name='share_create'),
]
