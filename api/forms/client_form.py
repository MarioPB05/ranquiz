from django import forms


class ClientForm(forms.Form):
    """Formulario para la creación de un cliente"""

    name = forms.CharField(max_length=100)
    surnames = forms.CharField(max_length=250)
    email = forms.EmailField()
    birthdate = forms.DateField()
    country = forms.CharField(max_length=200)
