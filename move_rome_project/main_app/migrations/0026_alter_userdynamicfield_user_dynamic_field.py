# Generated by Django 4.2 on 2024-01-13 23:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0025_userdynamicfield'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userdynamicfield',
            name='user_dynamic_field',
            field=models.IntegerField(),
        ),
    ]
