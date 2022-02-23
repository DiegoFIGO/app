# Generated by Django 3.2.7 on 2021-12-11 16:38

import ckeditor_uploader.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('erp', '0086_auto_20211210_1027'),
    ]

    operations = [
        migrations.AlterField(
            model_name='perfil',
            name='activities',
            field=ckeditor_uploader.fields.RichTextUploadingField(blank=True, max_length=10485760, null=True, verbose_name='9. Actividades'),
        ),
        migrations.AlterField(
            model_name='perfil',
            name='agreement',
            field=models.CharField(blank=True, max_length=7000, null=True, verbose_name='Convenio'),
        ),
        migrations.AlterField(
            model_name='perfil',
            name='goals',
            field=ckeditor_uploader.fields.RichTextUploadingField(blank=True, max_length=10485760, null=True, verbose_name='8. Metas'),
        ),
        migrations.AlterField(
            model_name='perfil',
            name='impact',
            field=models.CharField(blank=True, max_length=10485760, null=True, verbose_name='14. Impacto ambiental'),
        ),
        migrations.AlterField(
            model_name='perfil',
            name='indicators',
            field=ckeditor_uploader.fields.RichTextUploadingField(blank=True, max_length=10485760, null=True, verbose_name='13. Indicadores de resultados alcanzados: cualitativos y cuantitativos'),
        ),
        migrations.AlterField(
            model_name='perfil',
            name='management',
            field=models.CharField(blank=True, max_length=10485760, null=True, verbose_name='15. Autogestión y sostenibilidad'),
        ),
        migrations.AlterField(
            model_name='perfil',
            name='name',
            field=models.CharField(max_length=7000, verbose_name='1. Nombre del Proyecto (*)  '),
        ),
        migrations.AlterField(
            model_name='perfil',
            name='objectivs',
            field=ckeditor_uploader.fields.RichTextUploadingField(blank=True, max_length=10485760, null=True, verbose_name='7. Objetivos'),
        ),
        migrations.AlterField(
            model_name='perfil',
            name='schedule',
            field=ckeditor_uploader.fields.RichTextUploadingField(blank=True, max_length=10485760, null=True, verbose_name='10. Cronograma de actividades'),
        ),
    ]