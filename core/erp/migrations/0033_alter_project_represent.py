# Generated by Django 3.2.7 on 2021-11-12 05:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('erp', '0032_alter_project_represent'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='represent',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='erp.client', verbose_name='Representante'),
        ),
    ]
