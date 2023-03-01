"""Django v2.2 test project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
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
    path('dd/', include('django_dump_die.urls')),
    path('dd_tests/', include('django_dump_die.test_urls')),

    # DjangoETC routes for demo purposes.
    path('django_etc/', include('django_expanded_test_cases.test_urls')),

    # Default project root view.
    path('', include('settings.root_url')),
]
