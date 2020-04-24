# Generated by Django 3.0.3 on 2020-04-20 18:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('EAD_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='User_info',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=128)),
                ('last_name', models.CharField(max_length=128)),
                ('email', models.EmailField(max_length=264, unique=True)),
                ('role', models.CharField(choices=[('student', 'student'), ('dsa', 'DSA'), ('secy', 'secretary')], max_length=10)),
            ],
        ),
        migrations.DeleteModel(
            name='User',
        ),
    ]
