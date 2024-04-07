from django import forms
from django.forms import ModelForm
from api.models import Category


class CreateCategoryForm(ModelForm):
    """Formulario para crear una categoría."""

    name = forms.CharField(max_length=100)
    share_code = forms.CharField(max_length=20)

    class Meta:
        model = Category
        fields = '__all__'
