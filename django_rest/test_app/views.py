"""
Views for Django v4.2 test project app.
"""

# System Imports.
import json
import html
import re
import requests

# Third-Party Imports.
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import Group
from django.http import HttpResponse, JsonResponse, QueryDict
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.shortcuts import redirect, render, reverse
from rest_framework import permissions, viewsets

# Internal Imports.
from test_app.forms import ApiSendForm
from test_app.models import ApiRequestJson
from test_app.serializers import (
    GroupSerializer,
    UserSerializer,
)


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
    print('')
    print('api_parse():')

    # Get data from response.
    get_data = {}
    post_data = {}
    body_data = {}
    header_data = {}
    if request.headers:
        print('Received HEADERS:')
        header_data = dict(request.headers)
        print(header_data)
    if request.GET:
        print('Received GET:')
        get_data = _recurisive_json_parse(request.GET)
        for key, value in get_data.items():
            get_data[key] = value[0]
        print(get_data)
    if request.POST:
        print('Received POST:')
        post_data = _recurisive_json_parse(dict(request.POST))
        print(post_data)
    if request.body:
        print('Received BODY:')
        # Attempt to escape. Limited functionality so may not work.
        # To be precise, functions well with a standard JSON response.
        # But with any other response type that has a body, might break and be ugly.
        body_data = _recurisive_json_parse(html.unescape(request.body.decode('UTF-8')))
        print(body_data)
    print('\n')

    # Combine data.
    data = {}
    if header_data:
        data['HEADERS'] = header_data
    if get_data:
        data['GET'] = get_data
    if post_data:
        data['POST'] = post_data
    if body_data:
        data['body'] = body_data
    if not data:
        data = {'data': 'No data found in request.'}

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


def api_send(request):
    """Test app index page."""
    print('\n')
    print('api_send():')

    response_success = {}
    response_error = {}

    # Get initial data.
    form_initial = [{
        'is_str': True,
        'value': 'This is a test entry.'
    }]

    # Initialize formset.
    form = ApiSendForm()

    # Check if POST.
    if request.POST:
        # Is POST. Process data.
        print('Is POST submission.')

        data = request.POST
        form = ApiSendForm(data=data)

        if form.is_valid():
            # Handle for form submission.
            print('Submitted form data:')
            print('{0}'.format(form.cleaned_data))

            url = str(form.cleaned_data['url']).strip()
            get_params = str(form.cleaned_data.get('get_params', '')).strip()
            header_token = str(form.cleaned_data.get('header_token', '')).strip()
            payload = json.loads(str(form.cleaned_data.get('payload', {})).strip())

            # Determine url.
            if get_params and len(get_params) > 0:
                if url[-1] != '?' and get_params[0] != '?':
                    url += '?'
                url += get_params

            # Determine header values.
            headers = {'Accept': 'application/json'}
            if header_token:
                headers['token'] = header_token

            # Determine data values.
            if payload:
                data = json.dumps(payload)
            else:
                data = json.dumps({'success': True})

            # Generate API send object.
            is_error = False
            try:
                response = requests.post(
                    url,
                    headers=headers,
                    data=data,
                    timeout=5,
                )
            except Exception as err:
                is_error = True
                response_error['query_sent'] = False if not err.response else True
                response_error['message'] = str(err.message) if hasattr(err, 'message') else str(err)
                if 'Max retries exceeded with url' in response_error['message']:
                    response_error['help_text'] = (
                        'This error is often the result of a typo in the URL, or the desired endpoint being down. '
                        'Are you sure you entered the destination URL correctly?'
                    )

            if not is_error:
                # Handle for success state.

                response_success['status'] = response.status_code
                if response_success['status'] >= 400:
                    # Define help_text key now to preserve location in display ordering.

                    # Provide help text for some common error statuses.
                    if response_success['status'] == 400:
                        # 400: Bad Request
                        response_success['help_text'] = (
                            '400: Bad Request - This error is often the result of a bad or malformed request, such '
                            'as incorrect or unexpected syntax. Double check that the sent request data is correct.'
                        )
                    elif response_success['status'] == 401:
                        # 401: Unauthorized
                        response_success['help_text'] = (
                            '401: Unauthorized - This error is often the result of invalid or missing authentication '
                            'credentials. Are you sure the authentication tokens are correctly provided?'
                        )
                    elif response_success['status'] == 403:
                        # 403: Forbidden
                        response_success['help_text'] = (
                            '403: Forbidden - This error is often the result of invalid or missing authentication '
                            'credentials. Are you sure the authentication tokens are correctly provided?'
                        )
                    elif response_success['status'] == 404:
                        # 404: Not Found
                        response_success['help_text'] = (
                            '404: Not Found - This error is often the result of the requested url not existing on the '
                            'server. Are you sure you entered the destination URL correctly?'
                        )
                    elif response_success['status'] == 500:
                        # 500: Server Error
                        response_success['help_text'] = (
                            '500: Server Error - This error is often the result of your request being received, but '
                            'the server broke when trying to process the request. If this is a server you have '
                            'access to, then double check the server logs for more details.'
                        )

                if response.headers:
                    response_success['headers'] = response.headers
                if response.headers['content-Type'] and response.headers['Content-Type'] == 'application/json':
                    response_success['content'] = response.json()
                else:
                    content = html.unescape(response.content.decode('UTF-8'))

                    # NOTE: Below copied from Django ExpandedTestCase package.
                    # Replace html linebreak with actual newline character.
                    content = re.sub('<br>|</br>|<br/>|<br />', '\n', content)

                    # Replace non-breaking space with actual space character.
                    content = re.sub('(&nbsp;)+', ' ', content)

                    # Replace any carriage return characters with newline character.
                    content = re.sub(r'\r+', '\n', content)

                    # Replace any whitespace trapped between newline characters.
                    # This is empty/dead space, likely generated by how Django handles templating.
                    content = re.sub(r'\n\s+\n', '\n', content)

                    # Replace any repeating linebreaks.
                    content = re.sub(r'\n\n+', '\n', content)

                    # # Reduce any repeating whitespace instances.
                    # content = re.sub(r' ( )+', ' ', content)

                    # Strip final calculated string of extra outer whitespace.
                    content = str(content).strip()
                    response_success['content'] = content

                # Handle if was response was received, but it gave error level status.
                if response_success['status'] >= 400:
                    response_error = response_success
                    response_success = {}

    print('Rendering response...')
    print('')

    return render(request, 'test_app/api_send.html', {
        'form': form,
        'response_success': response_success,
        'response_error': response_error,
    })

# endregion API Views


# region REST API Views

class UserModelViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = get_user_model().objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class GroupModelViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]

# endregion REST API Views
