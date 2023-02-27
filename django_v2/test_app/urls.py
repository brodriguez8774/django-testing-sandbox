"""
Urls for Django v2.2 test project app.
"""

# Third-Party Imports.
from django.urls import include, path

# Internal Imports.
from . import views


app_name = 'test_app'
urlpatterns = [
    path('', views.index, name='index')
]
