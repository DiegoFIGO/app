# Generated by Django 3.2.7 on 2021-12-16 17:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('erp', '0090_alter_client_dni'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='desing',
            field=models.CharField(default=1, max_length=5000, verbose_name='Diseño de Proyecto (*) '),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='project',
            name='type_project',
            field=models.CharField(default=1, max_length=5000, verbose_name='Tipo de Proyecto (*) '),
            preserve_default=False,
        ),
    ]