# Generated by Django 4.2 on 2024-01-13 06:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0002_uploadedvideo'),
    ]

    operations = [
        migrations.AddField(
            model_name='uploadedvideo',
            name='video_image',
            field=models.URLField(default='empty', max_length=500),
        ),
    ]