# Generated by Django 3.2.7 on 2021-11-18 18:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('erp', '0042_auto_20211117_2329'),
    ]

    operations = [
        migrations.AddField(
            model_name='represent',
            name='job',
            field=models.CharField(default=1, max_length=150, verbose_name='Cargo dentro de la Institución'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='represent',
            name='profession',
            field=models.CharField(default=1, max_length=150, verbose_name='Título Académico'),
            preserve_default=False,
        ),
    ]
