# Generated by Django 3.2.7 on 2021-12-05 21:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('erp', '0070_auto_20211205_1637'),
    ]

    operations = [
        migrations.RenameField(
            model_name='certification',
            old_name='offer',
            new_name='document',
        ),
    ]
