# Generated by Django 4.2 on 2024-01-13 07:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0005_remove_uploadedvideo_video_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='uploadedvideo',
            name='video_image',
            field=models.URLField(default='data:image/jpeg;base64,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'),
        ),
    ]