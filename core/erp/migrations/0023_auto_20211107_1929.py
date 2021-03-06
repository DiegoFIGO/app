# Generated by Django 3.2.7 on 2021-11-08 00:29

import ckeditor.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('erp', '0022_auto_20211107_1920'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='description',
            field=models.CharField(max_length=255, verbose_name='Descripción'),
        ),
        migrations.AlterField(
            model_name='project',
            name='managed',
            field=ckeditor.fields.RichTextField(max_length=150, verbose_name='Introduccion'),
        ),
        migrations.AlterField(
            model_name='project',
            name='ogeneral',
            field=ckeditor.fields.RichTextField(max_length=150, verbose_name='Contenido'),
        ),
    ]
