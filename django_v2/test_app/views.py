"""
Views for Django v2.2 test project app.
"""

# Third-Party Imports.
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import redirect, render, reverse


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
    return render(request, 'test_app/login_check.html')


@permission_required('test_app.test_permission')
def view_with_permission_check(request):
    """Test view with basic User permission check."""
    return render(request, 'test_app/permission_check.html')


@login_required
def view_with_group_check(request):
    """Test view with basic User group check."""

    # Check group.
    user_groups = request.user.groups.all().values_list('name', flat=True)
    if 'test_group' not in user_groups and not request.user.is_superuser:
        return redirect(reverse('login'))

    return render(request, 'test_app/group_check.html')

# endregion Login/Permission Test Views
