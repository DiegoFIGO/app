# Generated by Django 3.2.7 on 2021-11-08 01:01

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('erp', '0025_auto_20211107_2000'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='managed',
            field=ckeditor.fields.RichTextField(max_length=15000, verbose_name='Introduccion'),
        ),
        migrations.AlterField(
            model_name='project',
            name='ogeneral',
            field=ckeditor.fields.RichTextField(max_length=65000, verbose_name='Contenido'),
        ),
    ]
