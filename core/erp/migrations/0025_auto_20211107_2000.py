# Generated by Django 3.2.7 on 2021-11-08 01:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('erp', '0024_auto_20211107_1957'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='managed',
            field=models.CharField(max_length=15000, verbose_name='Introduccion'),
        ),
        migrations.AlterField(
            model_name='project',
            name='ogeneral',
            field=models.CharField(max_length=65000, verbose_name='Contenido'),
        ),
    ]
