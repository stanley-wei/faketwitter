# Generated by Django 3.0.3 on 2020-03-12 19:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tweets', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='followed_users',
            field=models.CharField(default='', max_length=1000),
        ),
        migrations.AlterField(
            model_name='profile',
            name='liked_tweets',
            field=models.CharField(default='', max_length=1000),
        ),
    ]
