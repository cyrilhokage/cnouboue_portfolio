# Generated by Django 3.1.3 on 2021-01-16 11:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0007_post_html_content'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='html_content',
            field=models.TextField(blank=True, null=True),
        ),
    ]
