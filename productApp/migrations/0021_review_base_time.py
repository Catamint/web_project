# Generated by Django 4.2 on 2023-05-15 18:38

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ("productApp", "0020_alter_user_exp_favorite"),
    ]

    operations = [
        migrations.AddField(
            model_name="review_base",
            name="time",
            field=models.DateTimeField(
                default=django.utils.timezone.now, max_length=20, verbose_name="时间"
            ),
        ),
    ]
