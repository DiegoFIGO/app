# Generated by Django 3.2.7 on 2021-12-02 22:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('erp', '0063_remove_acquisitionbs_construcction'),
    ]

    operations = [
        migrations.AlterField(
            model_name='acquisitionbs',
            name='personal',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='erp.project', verbose_name='Seleccione nombre del proyecto'),
            preserve_default=False,
        ),
    ]
