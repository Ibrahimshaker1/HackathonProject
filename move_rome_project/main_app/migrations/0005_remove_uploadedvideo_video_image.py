# Generated by Django 4.2 on 2024-01-13 06:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0004_alter_uploadedvideo_video_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='uploadedvideo',
            name='video_image',
        ),
    ]
