# Generated by Django 4.0.5 on 2022-06-29 00:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0009_candidate_house'),
    ]

    operations = [
        migrations.AddField(
            model_name='candidate',
            name='sex',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
    ]
