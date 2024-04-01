"""
Django v2.2 test project URL Configuration
"""
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    # Django Admin views.
    path('admin/', admin.site.urls),

    # Django authentication views.
    path('accounts/', include('django.contrib.auth.urls')),

    # Basic/minimalistic Django application.
    path('test_app/', include('test_app.urls')),

    # Package testing views.

    # DjangoDD routes for demo purposes.
    # path('dd/', include('django_dump_die.urls')),
    # path('dd_tests/', include('django_dump_die.test_urls')),

    # DjangoETC routes for demo purposes.
    path('django_etc/', include('django_expanded_test_cases.test_urls')),

    # Default project root view.
    path('', include('settings.root_url')),
]
