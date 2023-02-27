"""
Views for Django v2.2 test project app.
"""

# Third-Party Imports.
from django.shortcuts import render


def root_project_home_page(request):
    """Shown for root page of entire project."""
    return render(request, 'test_app/root_project_home_page.html')


def index(request):
    """"""
    return render(request, 'test_app/index.html')
