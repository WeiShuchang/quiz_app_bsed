# Generated by Django 5.1 on 2024-10-12 16:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teacher', '0026_remove_fractiongamesession_correct_answers_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='fractiongamesession',
            name='selected_answers',
            field=models.JSONField(default=dict),
        ),
    ]