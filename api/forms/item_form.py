from django import forms
from django.forms import ModelForm
from api.models import List


class CreateItemForm(ModelForm):
    """Formulario para crear un item"""

    list = forms.ModelChoiceField(queryset=List.objects.all())
    name = forms.CharField(max_length=255)
    image = forms.ImageField(required=False)


class Meta:
    model = List
    fields = '__all__'
