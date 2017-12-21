# -*- coding: utf-8 -*-

from django import forms
from .validators import *

class DocumentForm(forms.Form):
    docfile = forms.FileField(
        label='Select a Csv file',
        allow_empty_file = False,
        validators = [MimetypeValidator(['text/csv','application/csv','text/plain'])],
        help_text="Upload a CSV file",
        
    )
