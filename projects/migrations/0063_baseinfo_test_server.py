# Generated by Django 3.2.10 on 2023-01-29 18:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0062_tourpics'),
    ]

    operations = [
        migrations.AddField(
            model_name='baseinfo',
            name='test_server',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
