# Generated by Django 2.0.6 on 2019-11-16 13:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_auto_20191116_1405'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='main_image',
            field=models.ImageField(blank=True, upload_to='images/'),
        ),
    ]
