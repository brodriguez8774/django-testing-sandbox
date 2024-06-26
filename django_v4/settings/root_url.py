"""
Root Url for Django v4.2 test project.
"""

# Third-Party Imports.
from django.urls import path

# Internal Imports.
from test_app.views import root_project_home_page


app_name = 'root_project_home_page'
urlpatterns = [
    path('', root_project_home_page, name='index')
]
