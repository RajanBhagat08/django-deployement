# Generated by Django 3.0.3 on 2020-04-21 09:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('EAD_app', '0007_auto_20200421_1421'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user_info',
            name='password',
        ),
    ]
