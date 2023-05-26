# Generated by Django 4.1.3 on 2023-05-26 20:02

import cropperjs.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("projects", "0073_reviewcard"),
    ]

    operations = [
        migrations.AddField(
            model_name="reviewcard",
            name="photo",
            field=cropperjs.models.CropperImageField(
                aspectratio=1, null=True, upload_to=""
            ),
        ),
    ]
