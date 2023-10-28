# Generated by Django 4.2 on 2023-05-08 16:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("productApp", "0013_alter_kind_base_kind"),
    ]

    operations = [
        migrations.AlterField(
            model_name="review_base",
            name="movie",
            field=models.ForeignKey(
                default=None,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="review",
                to="productApp.movie_base",
                verbose_name="电影",
            ),
        ),
    ]