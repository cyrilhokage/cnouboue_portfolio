# Generated by Django 3.1.3 on 2021-01-16 09:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("blog", "0006_auto_20201126_1406"),
    ]

    operations = [
        migrations.AddField(
            model_name="post",
            name="html_content",
            field=models.TextField(null=True),
        ),
    ]
