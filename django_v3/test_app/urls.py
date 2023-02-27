"""
Urls for Django v3.2 test project app.
"""

# Third-Party Imports.
from django.urls import include, path

# Internal Imports.
from . import views


app_name = 'test_app'
urlpatterns = [
    # Test views that have various login/permission requirements.
    path('view_with_login_check', views.view_with_login_check, name='view_with_login_check'),

    # App root.
    path('', views.index, name='index')
]
