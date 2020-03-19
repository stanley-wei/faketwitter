import datetime

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.files import File
from django.conf import settings

class Profile(models.Model):
    class Meta:
        permissions = [('can_post', 'can_delete_self_posts')]
    user_acc = models.OneToOneField(User, on_delete=models.CASCADE)
    user_handle = models.CharField(max_length=15)
    user_name = models.CharField(max_length=25, default="PH")
    user_bio = models.CharField(max_length=160, default="", blank = True)
    password = models.CharField(max_length=128, default="")
    acc_create_date = models.DateTimeField('date created', default = timezone.now)
    followed_users = models.CharField(max_length = 1000, default = "", blank = True)
    users_followed = models.IntegerField(default = 0)
    users_following = models.IntegerField(default = 0)
    liked_tweets = models.CharField(max_length = 1000, default = "", blank = True)
    profile_picture = models.ImageField(upload_to='profile_pictures/')
    def __str__(self):
        return self.user_name

class Tweet(models.Model):
    tweet_text = models.CharField(max_length=280, default = "")
    poster = models.ForeignKey(Profile, on_delete=models.CASCADE, default = 1)
    pub_date = models.DateTimeField('date published', default = timezone.now)
    likes = models.IntegerField(default = 0)
    def __str__(self):
        return self.tweet_text

class Reply(models.Model):
    tweet = models.ForeignKey(Tweet, on_delete=models.CASCADE)
    reply_text = models.CharField(max_length=280)
    reply_poster = models.ForeignKey(Profile, on_delete=models.CASCADE, default = 1)
    def __str__(self):
        return self.reply_text

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        newProfile = Profile.objects.create(user_acc=instance)
        newProfile.user_handle = instance.username
        newProfile.save()

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
