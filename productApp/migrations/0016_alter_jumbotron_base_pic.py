# Generated by Django 4.2 on 2023-05-13 09:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("productApp", "0015_jumbotron_base"),
    ]

    operations = [
        migrations.AlterField(
            model_name="jumbotron_base",
            name="pic",
            field=models.ImageField(default=None, null=True, upload_to="jumbotron/"),
        ),
    ]