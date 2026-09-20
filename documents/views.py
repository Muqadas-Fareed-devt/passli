from django.shortcuts import render

def documents_list_view(request):
    """Document vault list view."""
    return render(request, 'pages/landing.html')

def documents_upload_view(request):
    """Document upload view placeholder for Phase 3."""
    return render(request, 'pages/landing.html')
