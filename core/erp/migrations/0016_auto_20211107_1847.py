# Generated by Django 3.2.7 on 2021-11-07 23:47

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('erp', '0015_auto_20211107_1832'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='project',
            name='content',
        ),
        migrations.RemoveField(
            model_name='project',
            name='introduction',
        ),
        migrations.AlterField(
            model_name='project',
            name='description',
            field=ckeditor.fields.RichTextField(max_length=255, verbose_name='Descripción'),
        ),
    ]
