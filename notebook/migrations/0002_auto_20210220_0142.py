# Generated by Django 3.1.3 on 2021-02-20 01:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("notebook", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Program",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=60)),
                (
                    "format",
                    models.IntegerField(
                        choices=[
                            (0, "Film"),
                            (1, "Serie"),
                            (2, "Documentary"),
                            (3, "Comic book"),
                            (4, "Book"),
                        ],
                        default=0,
                    ),
                ),
                ("tags", models.CharField(max_length=90)),
                ("source", models.CharField(max_length=30)),
                ("release_date", models.DateTimeField()),
                ("available_date", models.DateTimeField()),
                (
                    "poster",
                    models.ImageField(
                        default="program_posters/poster_default.png",
                        upload_to="program_posters",
                    ),
                ),
            ],
        ),
        migrations.AlterField(
            model_name="profile",
            name="pic",
            field=models.ImageField(
                default="profile_pics/default.png", upload_to="profile_pics"
            ),
        ),
        migrations.CreateModel(
            name="View_program",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("date", models.DateTimeField()),
                ("chapter", models.CharField(max_length=10)),
                ("comment", models.TextField()),
                (
                    "status",
                    models.IntegerField(
                        choices=[(0, "To watch"), (1, "Watching"), (2, "Watched")],
                        default=0,
                    ),
                ),
                (
                    "profile",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="profile",
                        to="notebook.profile",
                    ),
                ),
                (
                    "program",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="program",
                        to="notebook.program",
                    ),
                ),
            ],
        ),
    ]
