import cloudinary
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
            self.fields['image_url'].initial = cloudinary.CloudinaryImage.build_url(instance.image) if instance.image else None
            self.fields['visibility'].initial = 'public' if instance.public else 'private'
            self.fields['categories'].initial = ','.join([category.category.name for category in instance.listcategory_set.all()])

    name = forms.CharField(
        max_length=70,
       widget=forms.TextInput(attrs={'class': 'form-control text-black', 'id': 'id_name', 'maxlength': '70', 'value': '', 'required': True})
    )
    image = forms.ImageField(required=False, widget=forms.FileInput(attrs={'class': 'form-control-file d-none', 'id': 'image'}))
    question = forms.CharField(
        max_length=100,
       widget=forms.TextInput(attrs={'class': 'form-control text-black', 'id': 'question', 'maxlength': '70', 'value': '¿Cúal prefieres?', 'required': True})
    )
    image_url = forms.CharField(
        required=False,
        max_length=100,
       widget=forms.TextInput(attrs={'class': 'd-none', 'id': 'image_url', 'maxlength': '70', 'value': '', 'required': False})
    )
    visibility = forms.ChoiceField(choices=[('public', 'Público'), ('private', 'Privado')],
                                   widget=forms.Select(attrs={
                                                              'class': 'form-select text-black',
                                                              'id': 'visibility', 'required': True,
                                                              'data-hide-search': 'true', 'data-control': 'select2'
                                                            }))
    categories = forms.CharField( widget=forms.TextInput(attrs={'class': 'd-none', 'id': 'categories'}))

    class Meta:
        model = List
        fields = ['name', 'image', 'question']
