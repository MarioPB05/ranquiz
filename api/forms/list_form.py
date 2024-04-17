from django import forms
from django.forms import ModelForm
from api.models import List


class CreateListForm(ModelForm):
    """Formulario para crear una lista"""

    name = forms.CharField(max_length=100)
    image = forms.ImageField(required=False)
    question = forms.CharField(
        max_length=100,
       widget=forms.TextInput(attrs={'class': 'form-control text-black', 'id': 'question', 'maxlength': '70', 'value': '¿Cúal prefieres?', 'required': True})
    )

    class Meta:
        model = List
        fields = ['name', 'image', 'question']
