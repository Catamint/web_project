# Generated by Django 4.2 on 2023-04-27 15:26

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="hall_base",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.TextField(max_length=500, verbose_name="名称")),
                ("total_seats", models.IntegerField(verbose_name="座位数")),
            ],
        ),
        migrations.CreateModel(
            name="movie_base",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.TextField(max_length=500, verbose_name="名称")),
                ("inform", models.TextField(verbose_name="简介")),
                (
                    "time_publish",
                    models.DateTimeField(
                        default=django.utils.timezone.now,
                        max_length=20,
                        verbose_name="上映时间",
                    ),
                ),
                ("photo", models.ImageField(blank=True, upload_to="movie/")),
                ("showing", models.BooleanField(default=False, verbose_name="正在上映")),
            ],
        ),
        migrations.CreateModel(
            name="product_data",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("text", models.TextField(blank=True, max_length=400, null=True)),
                ("photo", models.ImageField(blank=True, upload_to="product/")),
            ],
        ),
        migrations.CreateModel(
            name="session_base",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "time",
                    models.DateTimeField(
                        default=django.utils.timezone.now,
                        max_length=20,
                        verbose_name="时间",
                    ),
                ),
                (
                    "last_seats",
                    models.IntegerField(
                        blank=True, default=0, null=True, verbose_name="剩余座位数"
                    ),
                ),
                (
                    "charge",
                    models.IntegerField(blank=True, null=True, verbose_name="票价"),
                ),
                (
                    "location",
                    models.ForeignKey(
                        default="",
                        on_delete=django.db.models.deletion.PROTECT,
                        to="productApp.hall_base",
                        verbose_name="厅",
                    ),
                ),
                (
                    "movie",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="session",
                        to="productApp.movie_base",
                        verbose_name="电影",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="ticket_base",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("seat", models.IntegerField(verbose_name="座号")),
                (
                    "session",
                    models.OneToOneField(
                        default="",
                        on_delete=django.db.models.deletion.PROTECT,
                        to="productApp.session_base",
                        verbose_name="场次",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        default="",
                        on_delete=django.db.models.deletion.PROTECT,
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="用户",
                    ),
                ),
            ],
        ),
    ]