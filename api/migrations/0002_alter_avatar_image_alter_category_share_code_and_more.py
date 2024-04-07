# Generated by Django 4.2.11 on 2024-04-07 18:26

import api.models.model_template
import django.core.validators
from django.db import migrations, models
import shortuuid.django_fields


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='avatar',
            name='image',
            field=models.ImageField(upload_to='avatars/', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['png', 'jpg', 'jpeg']), api.models.model_template.validate_image_size]),
        ),
        migrations.AlterField(
            model_name='category',
            name='share_code',
            field=shortuuid.django_fields.ShortUUIDField(alphabet=None, length=20, max_length=20, prefix='CS'),
        ),
        migrations.AlterField(
            model_name='item',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='items/', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['png', 'jpg', 'jpeg']), api.models.model_template.validate_image_size]),
        ),
        migrations.AlterField(
            model_name='list',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='lists/', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['png', 'jpg', 'jpeg']), api.models.model_template.validate_image_size]),
        ),
        migrations.AlterField(
            model_name='list',
            name='share_code',
            field=shortuuid.django_fields.ShortUUIDField(alphabet=None, length=20, max_length=20, prefix='LS'),
        ),
        migrations.AlterField(
            model_name='user',
            name='share_code',
            field=shortuuid.django_fields.ShortUUIDField(alphabet=None, length=20, max_length=20, prefix='US'),
        ),
    ]
