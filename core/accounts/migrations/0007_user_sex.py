# Generated by Django 4.0.5 on 2022-06-29 00:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_rename_voted_for_co_user_voted_for_cob_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='sex',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
    ]