"""
Urls for Django REST test project app.
"""

# Third-Party Imports.
from django.urls import path
from rest_framework.authtoken import views as rest_views

# Internal Imports.
from . import views


app_name = 'test_app'
urlpatterns = [
    # Test views that have various login/permission requirements.
    path('view_with_login_check/', views.view_with_login_check, name='view_with_login_check'),
    path('view_with_permission_check/', views.view_with_permission_check, name='view_with_permission_check'),
    path('view_with_group_check/', views.view_with_group_check, name='view_with_group_check'),

    # Test API views.
    path('api/parse/', views.api_parse, name='api_parse'),
    path('api/display/', views.api_display, name='api_display'),
    path('api/send/', views.api_send, name='api_send'),

    # Test REST API views.
    path('api/api-token-auth', rest_views.obtain_auth_token, name='api_token_auth'),

    # Test app root, but as a class.
    path('as_class', views.ExampleClassView.as_view(), name='index_as_class'),
    # App root.
    path('', views.index, name='index')
]
