# Generated by Django 4.0.5 on 2022-07-03 16:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0011_candidate_no_votes'),
    ]

    operations = [
        migrations.RenameField(
            model_name='candidate',
            old_name='no_votes',
            new_name='no_votes_count',
        ),
    ]