# Generated by Django 3.2.7 on 2021-12-07 17:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('erp', '0079_auto_20211207_1143'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='construcction',
            name='benefits',
        ),
        migrations.RemoveField(
            model_name='construcction',
            name='resmaterials',
        ),
    ]
