# Generated by Django 3.0.3 on 2020-03-13 04:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tweets', '0005_auto_20200312_2136'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='profile_picture',
            field=models.ImageField(upload_to='profile_pictures/'),
        ),
    ]
