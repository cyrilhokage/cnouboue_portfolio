# Generated by Django 2.0.6 on 2019-11-15 14:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='context',
            field=models.IntegerField(choices=[(0, 'Private'), (1, 'School'), (2, 'Pro')], default=0),
        ),
        migrations.AddField(
            model_name='post',
            name='github_link',
            field=models.CharField(default='https://github.com/cyrilhokage', max_length=500),
        ),
        migrations.AddField(
            model_name='post',
            name='summary',
            field=models.CharField(default='https://github.com/cyrilhokage', max_length=500),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='post',
            name='technos',
            field=models.CharField(default=0, max_length=500),
            preserve_default=False,
        ),
    ]
