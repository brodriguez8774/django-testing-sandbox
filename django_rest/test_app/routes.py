"""
Urls for Django REST test project app.
"""


# System Imports.

# Third-Party Imports.
from rest_framework import routers

# Internal Imports.


from test_app import views
router = routers.DefaultRouter()

# Hyperlink API Views.

# Model API Views.
router.register(r'users', views.UserModelViewSet)
router.register(r'groups', views.GroupModelViewSet)
