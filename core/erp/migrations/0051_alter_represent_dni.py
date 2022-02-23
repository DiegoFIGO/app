# Generated by Django 3.2.7 on 2021-11-18 21:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('erp', '0050_alter_represent_dni'),
    ]

    operations = [
        migrations.AlterField(
            model_name='represent',
            name='dni',
            field=models.IntegerField(default=1, max_length=10, unique=True, verbose_name='Cédula'),
            preserve_default=False,
        ),
    ]
