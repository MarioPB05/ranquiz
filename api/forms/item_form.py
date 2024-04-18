import cloudinary
from django import forms
from django.forms import ModelForm
from api.models import Item


class CreateItemForm(ModelForm):
    """Formulario para crear un item"""

    def __init__(self, *args, **kwargs):
        instance = kwargs.get('instance')
        super(CreateItemForm, self).__init__(*args, **kwargs)
        if instance:
            # Si se proporciona una instancia, inicializa los campos con los valores de la instancia
            self.fields['name'].initial = instance.name
            self.fields['image_url'].initial = cloudinary.CloudinaryImage.build_url(instance.image) if instance.image else None

    name = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'class': 'form-control text-black item-name', 'id': 'id_template-name'}))
    image = forms.ImageField(required=False, widget=forms.FileInput(attrs={
        'class': 'd-none item-image', 'id': 'id_template-image'
    }), allow_empty_file=True)
    image_url = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'class': 'd-none item-image-url'
    }))

    class Meta:
        model = Item
        fields = ['name', 'image']
