from django import forms
from django.forms import ModelForm

from api.models import User


class LoginUserForm(forms.Form):
    """Formulario para iniciar sesión en la aplicación"""

    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control form-control-solid'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control form-control-solid'
    }))


class CreateUserForm(ModelForm):
    """Formulario para crear un usuario en la aplicación"""

    username = forms.CharField(max_length=50, widget=forms.TextInput(attrs={
        'class': 'form-control form-control-solid'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control form-control-solid'}))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control form-control-solid'}))

    def clean_username(self):
        """Comprueba que el nombre de usuario no esté en uso"""
        username = self.cleaned_data['username']

        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('El nombre de usuario ya está en uso')

        return username

    def clean(self):
        """Comprueba que las contraseñas sean iguales"""
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            self.add_error('confirm_password', 'Las contraseñas no coinciden')

        return cleaned_data

    def save(self, commit=True):
        """Guarda el usuario en la base de datos"""
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user

    class Meta:
        model = User
        fields = ['username', 'password']
