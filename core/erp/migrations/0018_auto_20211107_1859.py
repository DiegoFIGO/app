# Generated by Django 3.2.7 on 2021-11-07 23:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('erp', '0017_auto_20211107_1851'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='content',
            field=models.TextField(max_length=600, verbose_name='Contenidos'),
        ),
        migrations.AlterField(
            model_name='project',
            name='introduction',
            field=models.TextField(max_length=500, verbose_name='Introducción'),
        ),
    ]
