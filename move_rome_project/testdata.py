import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'move_rome_project.settings')
# from rest_framework.authtoken.models import Token

import django
django.setup()

from main_app import models
user = models.User.objects.all()
for my_user in user:
    # token, create = Token.objects.get_or_create(user=my_user)
    print(user)

