# Generated by Django 3.2.7 on 2021-12-05 21:37

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('erp', '0069_auto_20211202_2315'),
    ]

    operations = [
        migrations.CreateModel(
            name='Budget',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250, verbose_name='Nombre de Documento')),
                ('offer', models.FileField(blank=True, null=True, upload_to='perfilpdf/%Y/%m/%d', verbose_name='Presupuesto y PAC')),
                ('state', models.CharField(max_length=150, verbose_name='Año')),
                ('refomrs', models.FileField(blank=True, null=True, upload_to='perfilpdf/%Y/%m/%d', verbose_name='Reformas')),
                ('observations', models.CharField(max_length=1000, verbose_name='Prosupuesto')),
            ],
            options={
                'verbose_name': 'Presupuesto y PAC',
                'verbose_name_plural': 'Presupuesto y PACs',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Certification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250, verbose_name='Nombre de Proyecto')),
                ('certificate', models.CharField(max_length=150, verbose_name='Número de Certificado')),
                ('quantity', models.DecimalField(decimal_places=2, default=0.0, max_digits=10, verbose_name='Monto del Proyecto')),
                ('observations', models.CharField(max_length=1000, verbose_name='Observaciones de Proyecto')),
                ('offer', models.FileField(blank=True, null=True, upload_to='perfilpdf/%Y/%m/%d', validators=[django.core.validators.FileExtensionValidator(['pdf'])], verbose_name='Archivo de Proyecto')),
            ],
            options={
                'verbose_name': 'Certificación Presupuestaria',
                'verbose_name_plural': 'Certificaciones Presupuestarias',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Treasury',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250, verbose_name='Nombre de Proyecto')),
                ('offer', models.FileField(blank=True, null=True, upload_to='perfilpdf/%Y/%m/%d', verbose_name='Archivo de Proyecto')),
                ('state', models.CharField(max_length=150, verbose_name='Estado')),
                ('observations', models.CharField(max_length=1000, verbose_name='Observaciones de Proyecto')),
            ],
            options={
                'verbose_name': 'Tesoreria',
                'verbose_name_plural': 'Tesorerias',
                'ordering': ['id'],
            },
        ),
        migrations.AlterField(
            model_name='project',
            name='quantity',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10, verbose_name='Monto del Proyecto'),
        ),
    ]
