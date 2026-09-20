from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib import messages
from django.urls import reverse_lazy
from .forms import RegisterForm, LoginForm


def landing_view(request):
    """Public landing page view."""
    return render(request, 'pages/landing.html')


def register_view(request):
    """User registration view with auto-login on success."""
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f"Welcome to Passli, {user.username}! Your personal vault is ready.")
            return redirect('dashboard')
    else:
        form = RegisterForm()

    return render(request, 'accounts/register.html', {'form': form})


class CustomLoginView(LoginView):
    """Custom LoginView with custom template and authentication form."""
    template_name = 'accounts/login.html'
    authentication_form = LoginForm
    redirect_authenticated_user = True

    def form_valid(self, form):
        messages.success(self.request, f"Welcome back, {form.get_user().username}!")
        return super().form_valid(form)

    def get_success_url(self):
        return self.get_redirect_url() or reverse_lazy('dashboard')


class CustomLogoutView(LogoutView):
    """Custom LogoutView redirecting to landing page with message."""
    next_page = reverse_lazy('landing')

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            messages.info(request, "You have been securely signed out.")
        return super().dispatch(request, *args, **kwargs)


@login_required(login_url='login')
def dashboard_view(request):
    """
    Authenticated user personal vault dashboard.
    Displays vault statistics, active share passes, storage usage, and quick actions.
    """
    # Context data for documents and sharing apps (will be dynamically connected in Phase 3/4)
    total_docs = getattr(request.user, 'documents', None)
    total_docs_count = total_docs.count() if total_docs is not None else 0
    
    total_passes = getattr(request.user, 'share_passes', None)
    total_passes_count = total_passes.count() if total_passes is not None else 0
    active_passes_count = total_passes.filter(is_revoked=False).count() if total_passes is not None else 0

    context = {
        'total_documents': total_docs_count,
        'total_passes': total_passes_count,
        'active_passes': active_passes_count,
        'storage_used_mb': "0.0",
        'storage_quota_mb': "500.0",
        'storage_pct': 0,
        'recent_documents': [],
        'recent_passes': [],
    }
    return render(request, 'accounts/dashboard.html', context)
