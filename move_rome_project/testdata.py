import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'move_rome_project.settings')
# from rest_framework.authtoken.models import Token

import django
django.setup()

from main_app import models
videos = models.UploadedVideo.objects.all()
for video in videos:
    video.delete()

