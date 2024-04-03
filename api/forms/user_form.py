from django import forms


class UserForm(forms.Form):
    """Formulario para iniciar sesión en la aplicación"""

    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'placeholder': 'ranquiz@email.com',
        'class': 'form-control form-control-solid'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control form-control-lg form-control-solid'
    }))
