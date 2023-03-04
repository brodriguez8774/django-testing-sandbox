"""
Urls for Django v4.1 test project app.
"""

# Third-Party Imports.
from django.urls import path

# Internal Imports.
from . import views


app_name = 'test_app'
urlpatterns = [
    # Test views that have various login/permission requirements.
    path('view_with_login_check/', views.view_with_login_check, name='view_with_login_check'),
    path('view_with_permission_check/', views.view_with_permission_check, name='view_with_permission_check'),
    path('view_with_group_check/', views.view_with_group_check, name='view_with_group_check'),

    # App root.
    path('', views.index, name='index')
]
