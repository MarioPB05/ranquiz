# Generated by Django 4.2.11 on 2024-05-03 20:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0018_alter_listanswer_end_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listanswer',
            name='start_date',
            field=models.DateTimeField(),
        ),
    ]
