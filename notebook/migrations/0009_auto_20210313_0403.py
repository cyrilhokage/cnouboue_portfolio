# Generated by Django 3.1.3 on 2021-03-13 04:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("notebook", "0008_auto_20210313_0356"),
    ]

    operations = [
        migrations.AlterField(
            model_name="program",
            name="tmdb_id",
            field=models.IntegerField(blank=True, null=True, unique=True),
        ),
    ]
