# Generated by Django 3.2.7 on 2021-12-06 01:49

import ckeditor_uploader.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('erp', '0072_auto_20211205_1948'),
    ]

    operations = [
        migrations.AlterField(
            model_name='construcction',
            name='amount',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10, verbose_name='Monto del Proyecto'),
        ),
        migrations.AlterField(
            model_name='construcction',
            name='managed',
            field=ckeditor_uploader.fields.RichTextUploadingField(blank=True, max_length=20000, null=True, verbose_name='Antecedentes del Proyecto'),
        ),
        migrations.AlterField(
            model_name='construcction',
            name='ogeneral',
            field=ckeditor_uploader.fields.RichTextUploadingField(blank=True, max_length=65000, null=True, verbose_name='Detalle del Proyecto'),
        ),
    ]
