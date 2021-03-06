# Generated by Django 3.2.7 on 2022-02-22 21:15

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('erp', '0105_auto_20220222_1111'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='publics',
            name='created_at',
        ),
        migrations.RemoveField(
            model_name='publics',
            name='updated_at',
        ),
        migrations.AddField(
            model_name='construcction',
            name='hour',
            field=models.TimeField(default=datetime.datetime.now, verbose_name='Hora de Registro (*) '),
        ),
        migrations.AddField(
            model_name='employer',
            name='hour',
            field=models.TimeField(default=datetime.datetime.now, verbose_name='Hora de Registro (*) '),
        ),
        migrations.AddField(
            model_name='perfil',
            name='hour',
            field=models.TimeField(default=datetime.datetime.now, verbose_name='Hora de Registro (*) '),
        ),
        migrations.AddField(
            model_name='perfilprod',
            name='hour',
            field=models.TimeField(default=datetime.datetime.now, verbose_name='Hora de Registro (*) '),
        ),
        migrations.AddField(
            model_name='productive',
            name='hour',
            field=models.TimeField(default=datetime.datetime.now, verbose_name='Hora de Registro (*) '),
        ),
        migrations.AddField(
            model_name='project',
            name='hour',
            field=models.TimeField(default=datetime.datetime.now, verbose_name='Hora de Registro (*) '),
        ),
        migrations.AddField(
            model_name='publics',
            name='hour',
            field=models.TimeField(default=datetime.datetime.now, verbose_name='Hora de Registro (*) '),
        ),
    ]
