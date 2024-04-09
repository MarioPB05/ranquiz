from django import forms
from django.forms import ModelForm
from api.models import List


class CreateListForm(ModelForm):
    """Formulario para crear una lista"""

    name = forms.CharField(max_length=100)
    image = forms.ImageField(required=False)

    class Meta:
        model = List
        fields = ['name', 'image']
