# Generated by Django 5.1 on 2024-10-06 17:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teacher', '0014_gamesession_selected_answers'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='quizattempt',
            name='user',
        ),
        migrations.AddField(
            model_name='quizattempt',
            name='user_name',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
