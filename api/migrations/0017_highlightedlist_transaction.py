# Generated by Django 4.2.11 on 2024-05-01 11:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0016_item_creation_date_item_deleted_item_edit_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='highlightedlist',
            name='transaction',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='api.usertransaction'),
        ),
    ]
