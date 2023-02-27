
from django.urls import include, path

from . import views


app_name = 'test_app'
urlpatterns = [
    path('', views.index, name='index')
]
