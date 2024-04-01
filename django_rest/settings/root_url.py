"""
Root Url for Django REST test project.
"""

# Third-Party Imports.
from django.urls import path

# Internal Imports.
from test_app.views import root_project_home_page


app_name = 'root_project_home_page'
urlpatterns = [
    path('', root_project_home_page, name='index')
]
