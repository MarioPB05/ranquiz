from django import forms
from django.forms import ModelForm
from api.models import List


class CreateListForm(ModelForm):
    """Formulario para crear una lista"""

    def __init__(self, *args, **kwargs):
        instance = kwargs.get('instance')
        super(CreateListForm, self).__init__(*args, **kwargs)
        if instance:
            # Si se proporciona una instancia, inicializa los campos con los valores de la instancia
            self.fields['name'].initial = instance.name
            self.fields['question'].initial = instance.question

    name = forms.CharField(
        max_length=70,
       widget=forms.TextInput(attrs={'class': 'form-control text-black', 'id': 'id_name', 'maxlength': '70', 'value': '', 'required': True})
    )
    image = forms.ImageField(required=False)
    question = forms.CharField(
        max_length=100,
       widget=forms.TextInput(attrs={'class': 'form-control text-black', 'id': 'question', 'maxlength': '70', 'value': '¿Cúal prefieres?', 'required': True})
    )

    class Meta:
        model = List
        fields = ['name', 'image', 'question']
