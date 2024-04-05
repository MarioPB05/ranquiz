from django import forms
from django.forms import ModelForm

from api.models import Client


class CreateClientForm(ModelForm):
    """Formulario para la creación de un cliente"""

    name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control form-control-solid'}))
    surnames = forms.CharField(max_length=250, widget=forms.TextInput(attrs={'class': 'form-control form-control-solid'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'placeholder': 'ranquiz@email.com',
        'class': 'form-control form-control-solid'
    }))
    birthdate = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control form-control-solid'}))
    country = forms.CharField(max_length=200)

    def clean_email(self):
        """Comprueba que el email no esté en uso"""
        email = self.cleaned_data['email']

        if Client.objects.filter(email=email).exists():
            raise forms.ValidationError('El email ya está en uso')

        return email

    class Meta:
        model = Client
        fields = '__all__'
