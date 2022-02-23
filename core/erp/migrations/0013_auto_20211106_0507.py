# Generated by Django 3.2.7 on 2021-11-06 10:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('erp', '0012_auto_20211106_0405'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='managed',
            field=models.CharField(default=1, max_length=150, verbose_name='Población Objetivo'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='project',
            name='oespecific1',
            field=models.CharField(default=1, max_length=150, verbose_name='Objetivo Específico'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='project',
            name='ogeneral',
            field=models.CharField(default=2, max_length=150, verbose_name='Objetivo General'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='project',
            name='job',
            field=models.CharField(max_length=150, verbose_name='Cargo'),
        ),
        migrations.AlterField(
            model_name='project',
            name='name',
            field=models.CharField(max_length=150, verbose_name='Nombre del Proyecto'),
        ),
        migrations.AlterField(
            model_name='project',
            name='organization',
            field=models.CharField(max_length=150, verbose_name='Institución'),
        ),
    ]