from django import forms
from django.forms import ModelForm

from api.models import User, Avatar, Client


class LoginUserForm(forms.Form):
    """Formulario para iniciar sesión en la aplicación"""

    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'placeholder': 'ranquiz@email.com',
        'class': 'form-control form-control-solid'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control form-control-lg form-control-solid'
    }))


class CreateUserForm(ModelForm):
    """Formulario para crear un usuario en la aplicación"""

    username = forms.CharField(max_length=50)
    share_code = forms.CharField(max_length=20)
    avatar = forms.ModelChoiceField(queryset=Avatar.objects.all())
    client = forms.ModelChoiceField(queryset=Client.objects.all())

    def clean_username(self):
        """Comprueba que el nombre de usuario no esté en uso"""
        username = self.cleaned_data['username']

        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('El nombre de usuario ya está en uso')

        return username

    class Meta:
        model = User
        fields = '__all__'
