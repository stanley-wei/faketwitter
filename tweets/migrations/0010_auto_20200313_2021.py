# Generated by Django 3.0.3 on 2020-03-14 03:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tweets', '0009_profile_user_bio'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='users_followed',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='profile',
            name='users_following',
            field=models.IntegerField(default=0),
        ),
    ]
