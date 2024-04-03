from django import forms


class ClientForm(forms.Form):
    name = forms.CharField(max_length=100)
    surnames = forms.CharField(max_length=250)
    email = forms.EmailField()
    birthdate = forms.DateField()
    country = forms.CharField(max_length=200)
