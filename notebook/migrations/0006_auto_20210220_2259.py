# Generated by Django 3.1.3 on 2021-02-20 22:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("notebook", "0005_auto_20210220_2259"),
    ]

    operations = [
        migrations.AlterField(
            model_name="profile",
            name="slug",
            field=models.SlugField(default="default-slug-profile", max_length=70),
        ),
        migrations.AlterField(
            model_name="program",
            name="slug",
            field=models.SlugField(default="default-slug-program", max_length=70),
        ),
    ]
