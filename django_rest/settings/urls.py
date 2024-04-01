"""
Django REST test project URL Configuration
"""

# System Imports.

# Third-Party Imports.
from django.contrib import admin
from django.urls import include, path

# Internal Imports.
from test_app.routes import router


urlpatterns = [
    # Django Admin views.
    path('admin/', admin.site.urls),

    # Django authentication views.
    path('accounts/', include('django.contrib.auth.urls')),

    # Basic/minimalistic Django application.
    path('test_app/', include('test_app.urls')),

    # Django REST views.
    path('rest/', include(router.urls)),
    path('rest/api-auth/', include('rest_framework.urls')),

    # Package testing views.

    # AdminLTE2 routes for demo purposes.
    path('adminlte2/', include('adminlte2_pdq.urls')),

    # DjangoDD routes for demo purposes.
    path('dd/', include('django_dump_die.urls')),
    path('dd_tests/', include('django_dump_die.test_urls')),

    # DjangoETC routes for demo purposes.
    path('django_etc/', include('django_expanded_test_cases.test_urls')),

    # Default project root view.
    path('', include('settings.root_url')),
]
