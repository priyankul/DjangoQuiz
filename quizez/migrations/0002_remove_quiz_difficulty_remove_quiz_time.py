# Generated by Django 4.0.4 on 2022-04-17 17:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('quizez', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='quiz',
            name='difficulty',
        ),
        migrations.RemoveField(
            model_name='quiz',
            name='time',
        ),
    ]
