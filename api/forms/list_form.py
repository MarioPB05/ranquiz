from django import forms
from django.forms import ModelForm
from api.models import List


class CreateListForm(ModelForm):
    """Formulario para crear una lista"""

    owner = forms.ModelChoiceField(queryset=List.objects.all())
    share_code = forms.CharField(max_length=20)
    name = forms.CharField(max_length=100)
    public = forms.BooleanField(required=False)
    image = forms.ImageField(required=False)
    type = forms.ChoiceField(choices=List.TYPE_CHOICES)

    class Meta:
        model = List
        fields = '__all__'
