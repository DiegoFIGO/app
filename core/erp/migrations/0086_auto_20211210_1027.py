# Generated by Django 3.2.7 on 2021-12-10 15:27

import ckeditor_uploader.fields
import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('erp', '0085_alter_project_managed'),
    ]

    operations = [
        migrations.AlterField(
            model_name='acquisitionbs',
            name='observations',
            field=models.CharField(blank=True, max_length=1000, null=True, verbose_name='Observaciones de proyecto (*) '),
        ),
        migrations.AlterField(
            model_name='acquisitionbs',
            name='personal',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='erp.project', verbose_name='Seleccione nombre del proyecto (*) '),
        ),
        migrations.AlterField(
            model_name='acquisitionservices',
            name='observations',
            field=models.CharField(blank=True, max_length=10000, null=True, verbose_name='Observaciones de proyecto'),
        ),
        migrations.AlterField(
            model_name='acquisitionservices',
            name='personal',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='erp.project', verbose_name='Seleccione nombre del proyecto (*) '),
        ),
        migrations.AlterField(
            model_name='budget',
            name='name',
            field=models.CharField(max_length=250, verbose_name='Nombre de Documento (*) '),
        ),
        migrations.AlterField(
            model_name='budget',
            name='observations',
            field=models.CharField(max_length=1000, verbose_name='Presupuesto (*) '),
        ),
        migrations.AlterField(
            model_name='budget',
            name='state',
            field=models.CharField(max_length=150, verbose_name='Año (*) '),
        ),
        migrations.AlterField(
            model_name='category',
            name='desc',
            field=models.CharField(blank=True, max_length=700, null=True, verbose_name='Descripción'),
        ),
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(max_length=150, unique=True, verbose_name='Nombre (*) '),
        ),
        migrations.AlterField(
            model_name='certification',
            name='certificate',
            field=models.CharField(max_length=150, verbose_name='Número de Certificación (*) '),
        ),
        migrations.AlterField(
            model_name='certification',
            name='name',
            field=models.CharField(max_length=250, verbose_name='Nombre de Proyecto (*) '),
        ),
        migrations.AlterField(
            model_name='certification',
            name='observations',
            field=models.CharField(max_length=1000, verbose_name='Observaciones de Proyecto (*) '),
        ),
        migrations.AlterField(
            model_name='client',
            name='dni',
            field=models.IntegerField(max_length=10, unique=True, verbose_name='Cédula de Identidad (*) '),
        ),
        migrations.AlterField(
            model_name='client',
            name='email',
            field=models.EmailField(max_length=254, unique=True, verbose_name='Correo electrónico (*) '),
        ),
        migrations.AlterField(
            model_name='client',
            name='gender',
            field=models.CharField(choices=[('Masculino', 'Masculino'), ('Femenino', 'Femenino')], default='male', max_length=10, verbose_name='Sexo (*) '),
        ),
        migrations.AlterField(
            model_name='client',
            name='names',
            field=models.CharField(max_length=150, verbose_name='Nombres (*) '),
        ),
        migrations.AlterField(
            model_name='client',
            name='surnames',
            field=models.CharField(max_length=150, verbose_name='Apellidos (*) '),
        ),
        migrations.AlterField(
            model_name='construcction',
            name='benefits',
            field=models.CharField(blank=True, max_length=300000, null=True, verbose_name='Cliente Beneficiario'),
        ),
        migrations.AlterField(
            model_name='construcction',
            name='description',
            field=models.CharField(blank=True, max_length=255000, null=True, verbose_name='Descripción'),
        ),
        migrations.AlterField(
            model_name='construcction',
            name='managed',
            field=ckeditor_uploader.fields.RichTextUploadingField(blank=True, max_length=10485760, null=True, verbose_name='Antecedentes del Proyecto'),
        ),
        migrations.AlterField(
            model_name='construcction',
            name='name',
            field=models.CharField(max_length=1500, verbose_name='Proyecto (*) '),
        ),
        migrations.AlterField(
            model_name='construcction',
            name='ogeneral',
            field=ckeditor_uploader.fields.RichTextUploadingField(blank=True, max_length=10485760, null=True, verbose_name='Detalle del Proyecto'),
        ),
        migrations.AlterField(
            model_name='construcction',
            name='organization',
            field=models.CharField(max_length=1500, verbose_name='Entidad Ejecutora (*) '),
        ),
        migrations.AlterField(
            model_name='construcction',
            name='quantity_mount',
            field=models.CharField(blank=True, max_length=150, null=True, verbose_name='Detalle del Monto'),
        ),
        migrations.AlterField(
            model_name='construcction',
            name='representative',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='erp.represent', verbose_name='Administrador de Proyecto (*) '),
        ),
        migrations.AlterField(
            model_name='construcction',
            name='reshumans',
            field=models.CharField(max_length=150000, verbose_name='Recursos Humanos'),
        ),
        migrations.AlterField(
            model_name='construcction',
            name='resmaterials',
            field=models.CharField(blank=True, max_length=3000000, null=True, verbose_name='Recursos Materiales'),
        ),
        migrations.AlterField(
            model_name='construcction',
            name='results',
            field=models.CharField(blank=True, max_length=50000, null=True, verbose_name='Resultados'),
        ),
        migrations.AlterField(
            model_name='employer',
            name='dni',
            field=models.IntegerField(max_length=10, unique=True, verbose_name='Cédula de Identidad (*) '),
        ),
        migrations.AlterField(
            model_name='employer',
            name='email',
            field=models.EmailField(max_length=254, unique=True, verbose_name='Correo electrónico (*) '),
        ),
        migrations.AlterField(
            model_name='employer',
            name='names',
            field=models.CharField(max_length=150, verbose_name='Nombres completos (*)  '),
        ),
        migrations.AlterField(
            model_name='employer',
            name='nationality',
            field=models.CharField(max_length=150, verbose_name='Nacionalidad (*) '),
        ),
        migrations.AlterField(
            model_name='employer',
            name='position',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='erp.position', verbose_name='Cargo a ocupar (*) '),
        ),
        migrations.AlterField(
            model_name='employer',
            name='surnames',
            field=models.CharField(max_length=150, verbose_name='Apellidos completos (*) '),
        ),
        migrations.AlterField(
            model_name='informsuni',
            name='personal',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='erp.project', verbose_name='Seleccione nombre del proyecto para Informe de seguimiento (*) '),
        ),
        migrations.AlterField(
            model_name='position',
            name='area',
            field=models.CharField(blank=True, max_length=1000, null=True, verbose_name='Area estretégica del Cargo'),
        ),
        migrations.AlterField(
            model_name='position',
            name='desc',
            field=models.CharField(blank=True, max_length=1000, null=True, verbose_name='Descripción del Cargo'),
        ),
        migrations.AlterField(
            model_name='position',
            name='name_position',
            field=models.CharField(max_length=150, unique=True, verbose_name='Nombre del Cargo (*) '),
        ),
        migrations.AlterField(
            model_name='product',
            name='cat',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='erp.category', verbose_name='Categoría (*) '),
        ),
        migrations.AlterField(
            model_name='product',
            name='name',
            field=models.CharField(max_length=150, unique=True, verbose_name='Nombre (*) '),
        ),
        migrations.AlterField(
            model_name='product',
            name='stock',
            field=models.IntegerField(default=0, verbose_name='Stock (*)'),
        ),
        migrations.AlterField(
            model_name='project',
            name='description',
            field=models.CharField(blank=True, max_length=10485760, null=True, verbose_name='Descripción'),
        ),
        migrations.AlterField(
            model_name='project',
            name='name',
            field=models.CharField(max_length=5000, verbose_name='Proyecto *'),
        ),
        migrations.AlterField(
            model_name='project',
            name='ogeneral',
            field=ckeditor_uploader.fields.RichTextUploadingField(blank=True, max_length=10485760, null=True, verbose_name='Detalle del Proyecto'),
        ),
        migrations.AlterField(
            model_name='project',
            name='organization',
            field=models.CharField(max_length=5000, verbose_name='Entidad Ejecutora (*) '),
        ),
        migrations.AlterField(
            model_name='project',
            name='quantity_mount',
            field=models.CharField(blank=True, max_length=10485760, null=True, verbose_name='Detalle del Monto'),
        ),
        migrations.AlterField(
            model_name='project',
            name='representative',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='erp.represent', verbose_name='Administrador de Proyecto (*) '),
        ),
        migrations.AlterField(
            model_name='project',
            name='reshumans',
            field=models.CharField(blank=True, max_length=5000, null=True, verbose_name='Recursos Humanos'),
        ),
        migrations.AlterField(
            model_name='project',
            name='results',
            field=models.CharField(blank=True, max_length=10485760, null=True, verbose_name='Resultados'),
        ),
        migrations.AlterField(
            model_name='represent',
            name='address',
            field=models.CharField(blank=True, max_length=500, null=True, verbose_name='Dirección'),
        ),
        migrations.AlterField(
            model_name='represent',
            name='dni',
            field=models.IntegerField(max_length=10, unique=True, verbose_name='Cédula de Identidad (*) '),
        ),
        migrations.AlterField(
            model_name='represent',
            name='email',
            field=models.EmailField(max_length=254, unique=True, verbose_name='Correo electrónico (*) '),
        ),
        migrations.AlterField(
            model_name='represent',
            name='gender',
            field=models.CharField(choices=[('Masculino', 'Masculino'), ('Femenino', 'Femenino')], default='Masculino', max_length=10, verbose_name='Sexo'),
        ),
        migrations.AlterField(
            model_name='represent',
            name='job',
            field=models.CharField(max_length=150, verbose_name='Cargo dentro de la Institución (*)'),
        ),
        migrations.AlterField(
            model_name='represent',
            name='namesr',
            field=models.CharField(max_length=150, verbose_name='Nombres completos (*) '),
        ),
        migrations.AlterField(
            model_name='represent',
            name='profession',
            field=models.CharField(max_length=150, verbose_name='Título Académico (*) '),
        ),
        migrations.AlterField(
            model_name='represent',
            name='surnames',
            field=models.CharField(max_length=150, verbose_name='Apellidos completos (*) '),
        ),
        migrations.AlterField(
            model_name='servicesp',
            name='observations',
            field=models.CharField(max_length=10000, verbose_name='Observaciones de proyecto (*) '),
        ),
        migrations.AlterField(
            model_name='servicesp',
            name='personal',
            field=models.CharField(blank=True, max_length=10000, null=True, verbose_name='Detalles del personal'),
        ),
        migrations.AlterField(
            model_name='treasury',
            name='name',
            field=models.CharField(max_length=250, verbose_name='Nombre de Proyecto (*) '),
        ),
        migrations.AlterField(
            model_name='treasury',
            name='observations',
            field=models.CharField(max_length=1000, verbose_name='Observaciones de Proyecto (*) '),
        ),
        migrations.AlterField(
            model_name='treasury',
            name='state',
            field=models.CharField(max_length=150, verbose_name='Estado (*) asdvbn'),
        ),
        migrations.CreateModel(
            name='Perfil',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type_perfil', models.CharField(max_length=500, verbose_name='Tipo de Proyecto (*) ')),
                ('agreement', models.CharField(blank=True, max_length=700, null=True, verbose_name='Convenio')),
                ('month', models.CharField(blank=True, choices=[('Enero', 'Enero'), ('Febrero', 'Febrero'), ('Marzo', 'Marzo'), ('Abril', 'Abril'), ('Mayo', 'Mayo'), ('Junio', 'Junio'), ('Julio', 'Julio'), ('Agosto', 'Agosto'), ('Septiembre', 'Septiembre'), ('Octubre', 'Octubre'), ('Noviembre', 'Noviembre'), ('Diciembre', 'Diciembre')], default='Enero', max_length=20, null=True, verbose_name='Mes')),
                ('year', models.IntegerField(blank=True, max_length=4, null=True, unique=True, verbose_name='Año')),
                ('name', models.CharField(max_length=10485760, verbose_name='1. Nombre del Proyecto (*)  ')),
                ('location', models.CharField(blank=True, max_length=10485760, null=True, verbose_name='2. Localización geográfica')),
                ('analysis', models.CharField(blank=True, max_length=10485760, null=True, verbose_name='3. Análisis de la situación actual (diagnóstico)')),
                ('record', models.CharField(blank=True, max_length=10485760, null=True, verbose_name='4. Antecedentes')),
                ('justification', models.CharField(blank=True, max_length=10485760, null=True, verbose_name='5. Justificación')),
                ('relation', models.CharField(blank=True, max_length=10485760, null=True, verbose_name='6. Proyectos relacionados y / o complementarios')),
                ('objectivs', models.CharField(blank=True, max_length=10485760, null=True, verbose_name='7. Objetivos')),
                ('goals', models.CharField(blank=True, max_length=10485760, null=True, verbose_name='8. Metas')),
                ('activities', models.CharField(blank=True, max_length=10485760, null=True, verbose_name='9. Actividades')),
                ('schedule', models.CharField(blank=True, max_length=10485760, null=True, verbose_name='10. Cronograma de actividades')),
                ('duration', models.CharField(blank=True, max_length=10485760, null=True, verbose_name='11.  Duración del proyecto y vida útil')),
                ('beneficiaries', models.CharField(blank=True, max_length=10485760, null=True, verbose_name='12. Beneficiarios')),
                ('indicators', models.CharField(blank=True, max_length=10485760, null=True, verbose_name='13. Indicadores de resultados alcanzados: cualitativos y cuantitativos')),
                ('impact', ckeditor_uploader.fields.RichTextUploadingField(blank=True, max_length=10485760, null=True, verbose_name='14. Impacto ambiental')),
                ('management', ckeditor_uploader.fields.RichTextUploadingField(blank=True, max_length=10485760, null=True, verbose_name='15. Autogestión y sostenibilidad')),
                ('framework', ckeditor_uploader.fields.RichTextUploadingField(blank=True, max_length=10485760, null=True, verbose_name='16. Marco institucional')),
                ('financing', ckeditor_uploader.fields.RichTextUploadingField(blank=True, max_length=10485760, null=True, verbose_name='17. Financiamiento y análisis financiero del proyecto')),
                ('annexes', ckeditor_uploader.fields.RichTextUploadingField(blank=True, max_length=10485760, null=True, verbose_name='18. Anexos')),
                ('date_registration', models.DateField(default=datetime.datetime.now, verbose_name='Fecha de Registro (*) ')),
                ('date_start', models.DateField(blank=True, default=datetime.datetime.now, null=True, verbose_name='Fecha de inicio')),
                ('date_finish', models.DateField(blank=True, default=datetime.datetime.now, null=True, verbose_name='fecha de finalización')),
                ('new', models.BooleanField(verbose_name='Nuevo')),
                ('finished', models.BooleanField(verbose_name='Cumplido')),
                ('process', models.BooleanField(verbose_name='Proceso')),
                ('representative', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='erp.represent', verbose_name='Responsable del Proyecto (*) ')),
            ],
            options={
                'verbose_name': 'Proyecto',
                'verbose_name_plural': 'Proyectos',
                'ordering': ['id'],
            },
        ),
    ]