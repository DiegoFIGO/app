# Generated by Django 3.2.7 on 2021-11-16 21:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('erp', '0037_rename_names_represent_namesr'),
    ]

    operations = [
        migrations.RenameField(
            model_name='project',
            old_name='represent',
            new_name='representative',
        ),
    ]