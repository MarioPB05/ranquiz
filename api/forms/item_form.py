from django import forms
from django.forms import ModelForm
from api.models import Item


class CreateItemForm(ModelForm):
    """Formulario para crear un item"""

    name = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'class': 'form-control text-black item-name'}))
    image = forms.ImageField(required=False, widget=forms.FileInput(attrs={
        'class': 'd-none item-image'
    }), allow_empty_file=True)

    class Meta:
        model = Item
        fields = ['name', 'image']
