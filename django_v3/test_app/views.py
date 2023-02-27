"""
Views for Django v3.2 test project app.
"""

# Third-Party Imports.
from django.shortcuts import render


def index(request):
    """"""
    return render(request, 'test_app/index.html')
