# Generated by Django 3.2.7 on 2021-11-18 18:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('erp', '0043_auto_20211118_1305'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='project',
            name='job',
        ),
        migrations.RemoveField(
            model_name='project',
            name='profession',
        ),
    ]
