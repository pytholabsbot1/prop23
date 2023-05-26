# Generated by Django 3.2.10 on 2022-10-11 14:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0058_appleads'),
    ]

    operations = [
        migrations.AddField(
            model_name='floorplan',
            name='sold_out',
            field=models.BooleanField(default=False, null=True),
        ),
        migrations.AlterField(
            model_name='floorplan',
            name='plan',
            field=models.FileField(blank=True, null=True, upload_to=''),
        ),
    ]
