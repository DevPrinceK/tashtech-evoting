# Generated by Django 4.0.5 on 2022-06-28 23:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0008_alter_election_date_of_election'),
    ]

    operations = [
        migrations.AddField(
            model_name='candidate',
            name='house',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]
