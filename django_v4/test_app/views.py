"""
Views for Django v4.2 test project app.
"""

# System Imports.
import json
import html
import re
import requests

# Third-Party Imports.
from django.contrib.auth.decorators import login_required, permission_required
from django.http import JsonResponse, QueryDict
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.views.generic import TemplateView
from django.shortcuts import redirect, render, reverse

# Internal Imports.
from test_app.forms import ApiSendForm
from test_app.models import ApiRequestJson


# region Index/Root Views

def root_project_home_page(request):
    """Shown for root page of entire project."""
    return render(request, 'test_app/root_project_home_page.html')


def index(request):
    """Test app index page."""
    return render(request, 'test_app/index.html')


class ExampleClassView(TemplateView):
    """A basic Class Django view,
    with some of the more common built-in methods and documentation of what they do.

    Note: Some of these methods won't do anything with TemplateView. For example,
          the form valid/invalid methods require a class that will POST form data.
          Such as CreateView or UpdateView.
    """

    # Magic DjangoView args. Often times, can just define these and skip most method calls.

    # Template to render.
    template_name = 'test_app/index.html'

    # Url to use if redirecting.
    # If args/kwargs are needed, then probably need to use get_redirect_url() instead.
    url = None

    # If using a ModelView (ListView, DetailView, etc), these define what model data to call with.
    model = None
    queryset = None     # Can call more complicated query logic in get_queryset().

    # If using a ListView, this determines the number of results to display per page with pagination.
    paginate_by = 25

    # Params for views with form logic.
    form_class = None       # Form class to use.
    initial = {}            # Initial data to populate into form, if applicable.
    success_url = None      # If args/kwargs are needed, then probably need to use get_success_url() instead.

    def dispatch(self, request, *args, **kwargs):
        """Determines initial logic to call on view access.
        This is one of the first methods called by Django class views.
        This determines which of [GET(), POST(), etc] base class handling methods are called.
        If you need redirecting or other logic prior to calling these, do it here.

        If not redirecting outside of this class, then should probably always finish
        this function by returning a call to the original dispatch method.
        """
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        """Pulls additional context data to be used in the template."""

        # Get base context object.
        context = super().get_context_data(**kwargs)

        # Add new value to context.
        context['is_class_view'] = True

        # Return context.
        return context

    def get_queryset(self):
        """If using a view that uses models (DetailView, ListView, etc), then this modifies the default queryset."""
        queryset = super().get_queryset()

        # Use additional model query logic here.

        # Return our modified queryset.
        return queryset

    def get_ordering(self):
        """Return the field or fields to use for ordering the queryset."""

        # Replace this with a return to a single model field or list of model fields to order by.
        return super().get_ordering()

    def get(self, request, *args, **kwargs):
        """Handling for GET response type."""

        # Replace this with a response object.
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        """Handling for POST response type."""

        # Replace this with either a response object, or a call to
        # form_valid()/form_invalid() functions. Depending on what you need for class logic.
        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        """When processing a form, this is the logic to run on form validation success."""

        # Call parent logic. Should always include this line, as default views sometimes do additional processing.
        response = super().form_valid(form)

        # Do some handling with response here.

        # Return some response object for render.
        return response

    def form_invalid(self, form):
        """When processing a form, this is the logic to run on form validation failure."""

        # Call parent logic. Should always include this line, as default views sometimes do additional processing.
        response = super().form_invalid(form)

        # Do some handling with response here.

        # Return some response object for render.
        return response

    def get_success_url(self):
        """When processing a form, determines how to get the url for form success redirect."""

        # Replace this with a `reverse()` call to generate the correct URL.
        return super().get_success_url()

    def get_redirect_url(self, *args, **kwargs):
        """When handling a redirect view, this determines how to get the url."""

        # Replace this with a `reverse()` call to generate the correct URL.
        return super().get_redirect_url()

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
@require_http_methods(['GET', 'POST', 'PUT', 'PATCH', 'DELETE'])
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
    sent_data = {}

    # Initialize formset.
    form = ApiSendForm()

    # Check if POST.
    if request.POST:
        # Is POST. Process data.
        print('Is POST submission.')
        has_error = False

        post_data = request.POST
        form = ApiSendForm(data=post_data)

        if form.is_valid():
            # Handle for form submission.
            print('Submitted form data:')
            print('{0}'.format(form.cleaned_data))

            send_type = ''
            if 'submit_get' in post_data:
                send_type = 'GET'
                # data.pop('submit_get')
            if 'submit_post' in post_data:
                send_type = 'POST'
                # data.pop('submit_post')
            if 'submit_put' in post_data:
                send_type = 'PUT'
                # data.pop('submit_put')
            if 'submit_patch' in post_data:
                send_type = 'PATCH'
                # data.pop('submit_patch')
            if 'submit_delete' in post_data:
                send_type = 'DELETE'
                # data.pop('submit_delete')

            url = str(form.cleaned_data['url']).strip()
            get_params = str(form.cleaned_data.get('get_params', '')).strip()
            header_params = str(form.cleaned_data.get('header_params', '')).strip()
            payload = str(form.cleaned_data.get('payload', '{}')).strip()
            if len(payload) > 0:
                try:
                    payload = json.loads(payload)
                except json.decoder.JSONDecodeError:
                    has_error = True
                    payload = {}
                    form.add_error(
                        'payload',
                        'Unrecognized/invalid JSON syntax. Please double check syntax and try again.',
                    )
            else:
                has_error = True
                form.add_error(
                    'payload',
                    'Please provide JSON data to send. If API query is meant to be empty, use {}.',
                )

            # Determine url.
            if get_params and len(get_params) > 0:
                if url[-1] != '?' and get_params[0] != '?':
                    url += '?'
                url += get_params

            # Determine header values.
            headers = {'Accept': 'application/json'}
            if len(header_params) > 0:
                try:
                    header_params = json.loads(header_params)
                    headers.update(header_params)
                except json.decoder.JSONDecodeError:
                    has_error = True
                    payload = {}
                    form.add_error(
                        'header_params',
                        'Unrecognized/invalid JSON syntax. Please double check syntax and try again.',
                    )

            # Determine data values.
            if payload:
                data = json.dumps(payload)
            else:
                data = json.dumps({'success': True})

            # Generate API send object.
            try:
                # Generate based on clicked send button.
                if not has_error and send_type == 'GET':
                    response = requests.get(
                        url,
                        headers=headers,
                        data=data,
                        timeout=5,
                    )

                elif not has_error and send_type == 'POST':
                    response = requests.post(
                        url,
                        headers=headers,
                        data=data,
                        timeout=5,
                    )

                elif not has_error and send_type == 'PUT':
                    response = requests.put(
                        url,
                        headers=headers,
                        data=data,
                        timeout=5,
                    )

                elif not has_error and send_type == 'PATCH':
                    response = requests.patch(
                        url,
                        headers=headers,
                        data=data,
                        timeout=5,
                    )

                elif not has_error and send_type == 'DELETE':
                    response = requests.delete(
                        url,
                        headers=headers,
                        data=data,
                        timeout=5,
                    )

                elif not has_error:
                    # Unknown send type. Somehow. Raise error.
                    form.add_error(None, 'Invalid send_type. Was "{0}".'.format(send_type))
            except Exception as err:
                has_error = True
                response_error['query_sent'] = False if not err.response else True
                response_error['message'] = str(err.message) if hasattr(err, 'message') else str(err)
                if 'Max retries exceeded with url' in response_error['message']:
                    response_error['help_text'] = (
                        'This error is often the result of a typo in the URL, or the desired endpoint being down. '
                        'Are you sure you entered the destination URL correctly?'
                    )

            if not has_error:
                # Handle for success state.

                # Display sent input data to user.
                # That way they can change the form for a subsequent request and still see what was sent last time.
                sent_data['send_type'] = send_type
                sent_data['url'] = url
                sent_data['headers'] = headers
                sent_data['content'] = data

                # Parse returned response status code.
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
                    elif response_success['status'] == 405:
                        # 405: Method Not Allowed
                        response_success['help_text'] = (
                            '405: Method Not Allowed - This error is often the result of the destination understanding '
                            'the sent response type (GET/POST/PUT/PATCH/DELETE), but not supporting said type. '
                            'If this is a server you have access to, then double check that the endpoint is configured '
                            'correctly.'
                        )
                    elif response_success['status'] == 415:
                        # 415: Unsupported Media Type
                        response_success['help_text'] = (
                            '415: Unsupported Media Type - This error is often the result of the destination '
                            'being unable to parse the provided content. Are you sure the payload was entered '
                            'correctly?'
                        )
                    elif response_success['status'] == 500:
                        # 500: Server Error
                        response_success['help_text'] = (
                            '500: Server Error - This error is often the result of your request being received, but '
                            'the server broke when trying to process the request. If this is a server you have '
                            'access to, then double check the server logs for more details.'
                        )

                # Parse returned response header data.
                if response.headers:
                    response_success['headers'] = response.headers

                # Parse returned response content.
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
        'sent_data': sent_data,
        'response_success': response_success,
        'response_error': response_error,
    })

# endregion API Views
