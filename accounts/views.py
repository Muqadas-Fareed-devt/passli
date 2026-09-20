from django.shortcuts import render
from django.contrib.auth.views import LoginView, LogoutView

def landing_view(request):
    """Public landing page view."""
    return render(request, 'pages/landing.html')

def register_view(request):
    """Placeholder registration view for Phase 2."""
    return render(request, 'pages/landing.html')

def dashboard_view(request):
    """Placeholder dashboard view for Phase 2."""
    return render(request, 'pages/landing.html')
