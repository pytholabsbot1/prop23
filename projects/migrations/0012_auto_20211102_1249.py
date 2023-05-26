# Generated by Django 3.2.8 on 2021-11-02 12:49

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0011_auto_20211102_1115'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='bathrooms',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='listing',
            name='brochure',
            field=models.FileField(null=True, upload_to=''),
        ),
        migrations.AddField(
            model_name='listing',
            name='open_area',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='listing',
            name='total_units',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='listing',
            name='completion_date',
            field=models.DateField(default=datetime.datetime(2021, 11, 2, 12, 49, 50, 352442)),
        ),
    ]
