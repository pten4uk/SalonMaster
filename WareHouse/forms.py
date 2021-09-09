from django import forms

from .models import *


class MaterialForm(forms.ModelForm):
    class Meta:
        model = Material
        fields = ['brand', 'category', 'number', 'volume']


class UpdateForm(forms.Form):
    packages = forms.IntegerField(min_value=0, required=False)
    quantity = forms.IntegerField(min_value=0, required=False)
