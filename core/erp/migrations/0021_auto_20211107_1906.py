# Generated by Django 3.2.7 on 2021-11-08 00:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('erp', '0020_auto_20211107_1905'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='project',
            name='contentpro',
        ),
        migrations.RemoveField(
            model_name='project',
            name='introductionpro',
        ),
    ]
