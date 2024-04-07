from django import forms
from django.forms import ModelForm
from api.models import List


class CreateItemForm(ModelForm):
    """Formulario para crear un item"""

    list = forms.ModelChoiceField(queryset=List.objects.all())
    name = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'class': 'form-control text-black item-name'}))
    image = forms.ImageField(required=False, widget=forms.FileInput(attrs={'class': 'd-none item-image'}))

    class Meta:
        model = List
        fields = '__all__'
