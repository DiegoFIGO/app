# Generated by Django 3.2.7 on 2021-12-03 03:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('erp', '0066_auto_20211202_2224'),
    ]

    operations = [
        migrations.AlterField(
            model_name='informsuni',
            name='personal',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='erp.project'),
        ),
    ]
