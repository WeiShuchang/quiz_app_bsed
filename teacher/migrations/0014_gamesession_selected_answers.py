# Generated by Django 5.1 on 2024-10-06 07:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teacher', '0013_choice_picture'),
    ]

    operations = [
        migrations.AddField(
            model_name='gamesession',
            name='selected_answers',
            field=models.JSONField(default=dict),
        ),
    ]