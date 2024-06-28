"""
App definition for Django v4.2 test project app.
"""

# Third-Party Imports.
from django.apps import AppConfig


class TestAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'test_app'
