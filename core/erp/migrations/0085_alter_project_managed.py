# Generated by Django 3.2.7 on 2021-12-09 18:05

import ckeditor_uploader.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('erp', '0084_auto_20211208_2354'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='managed',
            field=ckeditor_uploader.fields.RichTextUploadingField(blank=True, max_length=10485760, null=True, verbose_name='Antecedentes del Proyecto'),
        ),
    ]