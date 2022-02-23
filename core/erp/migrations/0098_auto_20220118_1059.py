# Generated by Django 3.2.7 on 2022-01-18 15:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('erp', '0097_rename_project_servicesp_project_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='servicesp',
            name='project_name',
        ),
        migrations.AddField(
            model_name='servicesp',
            name='personals',
            field=models.CharField(blank=True, max_length=10000, null=True, verbose_name='Detalles del personal'),
        ),
        migrations.AlterField(
            model_name='servicesp',
            name='personal',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='erp.project', verbose_name='Seleccione nombre del proyecto (*)'),
            preserve_default=False,
        ),
    ]