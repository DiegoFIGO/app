# Generated by Django 3.2.7 on 2022-02-21 00:35

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('erp', '0102_alter_construcction_date_emission'),
    ]

    operations = [
        migrations.AlterField(
            model_name='construcction',
            name='date_emission',
            field=models.DateField(default=datetime.datetime.now, verbose_name='Fecha de emisión'),
        ),
    ]
