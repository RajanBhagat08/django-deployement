# Generated by Django 3.0.3 on 2020-04-23 21:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('EAD_app', '0032_auto_20200424_0250'),
    ]

    operations = [
        migrations.AlterField(
            model_name='venue',
            name='requested_venue_student',
            field=models.CharField(blank=True, choices=[('Lab-303', 'lab-303'), ('Lab-306', 'lab-306'), ('Lab-307', 'lab-307'), ('CL-13', 'CL-13'), ('CL-14', 'CL-14')], max_length=20, null=True),
        ),
    ]
