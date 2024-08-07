"""
Forms for Django v2.2 test project app.
"""

# System Imports.

# Third-Party Imports.
from django import forms

# Internal Imports.


class ApiSendForm(forms.Form):
    """A single line item for sending in an API call."""

    url = forms.URLField()
    get_params = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'rows': '6'}),
        help_text='Optional URL get param to append to URL.',
    )
    header_params = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'rows': '6'}),
        help_text='Optional dict of data to put into request header, such as values required for API authentication.'
    )
    payload = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'rows': '20'}),
        help_text=(
            'Should be in proper JSON dictionary format or else will error. <br><br>'
            'Ex: Use double quotes instead of single, booleans should be lower case, etc. <br><br>'
            'If left empty, will send <br>{"success": true}.'
        )
    )
