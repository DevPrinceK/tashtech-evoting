# Generated by Django 4.0.5 on 2022-06-25 10:30

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0006_election_is_active'),
    ]

    operations = [
        migrations.AlterField(
            model_name='election',
            name='date_of_election',
            field=models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True),
        ),
    ]
