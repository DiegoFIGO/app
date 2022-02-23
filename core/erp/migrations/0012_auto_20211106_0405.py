# Generated by Django 3.2.7 on 2021-11-06 09:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('erp', '0011_project_academic'),
    ]

    operations = [
        migrations.RenameField(
            model_name='project',
            old_name='academic',
            new_name='job',
        ),
        migrations.AddField(
            model_name='project',
            name='profession',
            field=models.CharField(default=1, max_length=150, verbose_name='Título Academico'),
            preserve_default=False,
        ),
    ]