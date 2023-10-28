# Generated by Django 4.2 on 2023-05-08 11:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("productApp", "0009_alter_picture_base_movie"),
    ]

    operations = [
        migrations.AlterField(
            model_name="movie_base",
            name="name",
            field=models.CharField(max_length=500, verbose_name="名称"),
        ),
        migrations.AlterField(
            model_name="picture_base",
            name="movie",
            field=models.ForeignKey(
                default=None,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="pictures",
                to="productApp.movie_base",
                verbose_name="电影",
            ),
        ),
        migrations.AlterField(
            model_name="picture_base",
            name="name",
            field=models.CharField(default="剧照", max_length=50),
        ),
    ]
