# Generated by Django 4.1.7 on 2023-03-17 22:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('music', '0002_report'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='music',
            name='likes',
        ),
        migrations.AddField(
            model_name='music',
            name='likes',
            field=models.IntegerField(default=0),
        ),
    ]
