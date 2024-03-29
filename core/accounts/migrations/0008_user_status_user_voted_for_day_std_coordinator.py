# Generated by Django 4.0.5 on 2023-07-04 20:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0007_user_sex'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='status',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='voted_for_day_std_coordinator',
            field=models.BooleanField(default=False),
        ),
    ]
