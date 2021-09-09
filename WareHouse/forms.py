from django import forms

from .models import *


class MaterialForm(forms.ModelForm):
    class Meta:
        model = Material
        fields = ['brand', 'category', 'number', 'volume', 'quantity']


class UpdateForm(forms.Form):
    quantity = forms.IntegerField(min_value=0)


class ChoiceCategoryForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].empty_label = 'Не выбрана'
    
    class Meta:
        model = Material
        fields = ['category']