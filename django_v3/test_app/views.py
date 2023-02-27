"""
Views for Django v3.2 test project app.
"""

# Third-Party Imports.
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render


# region Index/Root Views

def root_project_home_page(request):
    """Shown for root page of entire project."""
    return render(request, 'test_app/root_project_home_page.html')


def index(request):
    """Test app index page."""
    return render(request, 'test_app/index.html')

# endregion Index/Root Views


# region Login/Permission Test Views

@login_required
def view_with_login_check(request):
    """Test view with basic login check."""
    return render(request, 'test_app/index.html')

@permission_required('TODO: Add permission check')
def view_with_permission_check(request):
    """Test view with basic User permission check."""
    return render(request, 'test_app/index.html')

# TODO: Add group check.
def view_with_group_check(request):
    """Test view with basic User group check."""
    return render(request, 'test_app/index.html')

# endregion Login/Permission Test Views
