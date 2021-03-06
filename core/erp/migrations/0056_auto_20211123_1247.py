# Generated by Django 3.2.7 on 2021-11-23 17:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('erp', '0055_employer_position'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='employer',
            options={'ordering': ['id'], 'verbose_name': 'Empleado', 'verbose_name_plural': 'Empleados'},
        ),
        migrations.AlterModelOptions(
            name='position',
            options={'ordering': ['id'], 'verbose_name': 'Cargo', 'verbose_name_plural': 'Cargos'},
        ),
        migrations.AlterField(
            model_name='employer',
            name='finished',
            field=models.BooleanField(verbose_name='Inactivo'),
        ),
        migrations.AlterField(
            model_name='employer',
            name='new',
            field=models.BooleanField(verbose_name='Activo'),
        ),
    ]
