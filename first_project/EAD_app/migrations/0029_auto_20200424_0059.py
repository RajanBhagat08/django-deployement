# Generated by Django 3.0.3 on 2020-04-23 19:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('EAD_app', '0028_auto_20200423_2219'),
    ]

    operations = [
        migrations.RenameField(
            model_name='venue',
            old_name='app_by_oi',
            new_name='app_by_ois',
        ),
        migrations.AlterField(
            model_name='venue',
            name='requested_venue_secy',
            field=models.CharField(blank=True, choices=[('l26', 'LH-26'), ('l27', 'LH-27'), ('l28', 'LH-28'), ('Auditorium', 'Auditorium'), ('Audi With Arena', 'Audi Arena')], max_length=20, null=True),
        ),
    ]
