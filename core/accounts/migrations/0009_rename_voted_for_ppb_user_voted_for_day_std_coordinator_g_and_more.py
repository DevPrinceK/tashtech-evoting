# Generated by Django 4.0.5 on 2023-07-04 23:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0008_user_status_user_voted_for_day_std_coordinator'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='voted_for_ppb',
            new_name='voted_for_day_std_coordinator_g',
        ),
        migrations.RenameField(
            model_name='user',
            old_name='voted_for_ppg',
            new_name='voted_for_uafb',
        ),
        migrations.AddField(
            model_name='user',
            name='voted_for_uafg',
            field=models.BooleanField(default=False),
        ),
    ]
