# Generated by Django 4.2.11 on 2024-04-13 14:28

from django.db import migrations, models
import shortuuid.django_fields


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0008_user_money'),
    ]

    operations = [
        migrations.AddField(
            model_name='award',
            name='color',
            field=models.CharField(default='color', max_length=50),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='notification',
            name='share_code',
            field=shortuuid.django_fields.ShortUUIDField(alphabet=None, length=18, max_length=20, prefix='NT'),
        ),
    ]
