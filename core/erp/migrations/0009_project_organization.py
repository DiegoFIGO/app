# Generated by Django 3.2.4 on 2021-09-21 22:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('erp', '0008_rename_project_project_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='organization',
            field=models.CharField(default=2, max_length=150, verbose_name='Entidad'),
            preserve_default=False,
        ),
    ]