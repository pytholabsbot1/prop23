# Generated by Django 3.2.10 on 2023-01-30 07:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0068_alter_floorplantype_yt_link'),
    ]

    operations = [
        migrations.AlterField(
            model_name='floorplan',
            name='tp',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='projects.floorplantype'),
        ),
    ]
