# Generated by Django 5.1 on 2024-09-21 09:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0002_delete_studentclass'),
        ('teacher', '0008_delete_studentclass'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='category',
            name='class_assigned',
        ),
        migrations.DeleteModel(
            name='Class',
        ),
    ]
