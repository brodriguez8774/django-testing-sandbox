"""
Views for Django v4.1 test project app.
"""

# System Imports.
import json
import html

# Third-Party Imports.
from django.contrib.auth.decorators import login_required, permission_required
from django.http import JsonResponse, QueryDict
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.shortcuts import redirect, render, reverse

# Internal Imports.
from test_app.models import ApiRequestJson


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


# region API Views

@csrf_exempt
@require_http_methods(["GET", "POST"])
def api_parse(request):
    """Takes in JSON ping, and saves incoming value to web cookies.

    Then if api_display view is called after, will display the saved cookie value to web page.

    Allows quick debugging to make sure the expected, correct data is being sent.
    """
    # Get data from response.
    data = {'data': 'No data found in request.'}
    if request.GET:
        data = request.GET
    elif request.POST:
        data = dict(request.POST)
    elif request.body:
        # Attempt to escape. Limited functionality so may not work.
        data = html.unescape(request.body.decode('UTF-8'))

    data = _recurisive_json_parse(data)

    # Save api data to database.
    model_instance = ApiRequestJson.objects.first()
    if not model_instance:
        model_instance = ApiRequestJson.objects.create()
    model_instance.json_value = data
    model_instance.save()

    # Generate response.
    return JsonResponse({'success': True})


def _recurisive_json_parse(data_item):
    """Helper function to ensure all sub-items of response are properly read-in."""

    # Convert from potentially problematic types, for easier handling.
    if isinstance(data_item, QueryDict):
        data_item = dict(data_item)
    if isinstance(data_item, tuple):
        data_item = list(data_item)

    # Process some known types.
    if isinstance(data_item, dict):
        # Is dictionary. Iterate over each (key, value) pair and attempt to convert.
        for key, value in data_item.items():
            data_item[key] = _recurisive_json_parse(value)

    elif isinstance(data_item, list):
        # Is iterable. Iterate over each item and attempt to convert.
        for index in range(len(data_item)):
            sub_item = data_item[index]
            data_item[index] = _recurisive_json_parse(sub_item)

    else:
        # For all other types, just attempt naive conversion
        try:
            data_item = json.loads(data_item)
        except:
            # On any failure, just skip. Leave item as-is.
            pass

    # Return parsed data.
    return data_item


def api_display(request):
    """After a JSON ping to api_parse view, this displays parsed value to web page.

    Allows quick debugging to make sure the expected, correct data is being sent.
    """

    # Grab api data from session, if any.
    model_instance = ApiRequestJson.objects.first()
    if model_instance:
        content = {
            'payload_data': model_instance.json_value,
            'payload_sent_at': model_instance.date_created,
        }
    else:
        content = {
            'payload_data': {},
            'payload_sent_at': 'N/A',
        }

    # Attempt to output api data to browser.
    response = JsonResponse(content, safe=False)

    # Delete all existing instances of saved API data.
    ApiRequestJson.objects.all().delete()

    # Return data view to user.
    return response

# endregion API Views
