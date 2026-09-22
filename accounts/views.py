from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib import messages
from django.urls import reverse_lazy
from django.db.models import Sum
from .forms import RegisterForm, LoginForm
from documents.models import Document
from sharing.models import SharePass


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
    user_docs = Document.objects.filter(user=request.user)
    total_docs_count = user_docs.count()
    
    # Calculate storage
    total_bytes = user_docs.aggregate(total=Sum('file_size'))['total'] or 0
    storage_used_mb = total_bytes / (1024 * 1024)
    storage_quota_mb = 500.0  # 500 MB default vault quota
    storage_pct = min(100, int((storage_used_mb / storage_quota_mb) * 100)) if storage_quota_mb > 0 else 0

    # Share passes metrics
    all_passes = SharePass.objects.filter(owner=request.user).prefetch_related('documents').order_by('-created_at')
    total_passes_count = all_passes.count()
    active_passes = [p for p in all_passes if p.is_active()]
    active_passes_count = len(active_passes)
    recent_passes = active_passes[:4]

    recent_documents = user_docs.order_by('-created_at')[:4]

    context = {
        'total_documents': total_docs_count,
        'total_passes': total_passes_count,
        'active_passes': active_passes_count,
        'storage_used_mb': f"{storage_used_mb:.1f}",
        'storage_quota_mb': f"{storage_quota_mb:.0f}",
        'storage_pct': storage_pct,
        'recent_documents': recent_documents,
        'recent_passes': recent_passes,
    }
    return render(request, 'accounts/dashboard.html', context)
