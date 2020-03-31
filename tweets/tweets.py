from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

import random
from .models import *
from .database import *
from .users import findLoggedInUser

def makeNewTweet(request):
    logged_In_User = findLoggedInUser(request)
    newTweet = Tweet(tweet_text = request.POST.get('tweet_text'), poster = logged_In_User)
    newTweet.save()
    return newTweet

@login_required(login_url='tweets/login/')
def LikeTweet(request, tweet_id):
    logged_In_User = findLoggedInUser(request)
    liked_tweets = logged_In_User.liked_tweets
    if str(tweet_id) not in liked_tweets.split(','):
        liked_tweets += str(tweet_id) + ","
        logged_In_User.liked_tweets = liked_tweets
        logged_In_User.save()

        tweet = findTweetById(tweet_id)
        tweet.likes += 1
        tweet.save()

@login_required(login_url='tweets/login/')
def UnlikeTweet(request, tweet_id):
    logged_In_User = findLoggedInUser(request)
    liked_tweets = logged_In_User.liked_tweets.split(',')
    if str(tweet_id) in liked_tweets:
        while str(tweet_id) in liked_tweets:
            liked_tweets.remove(str(tweet_id))
        liked_tweets = ','.join(liked_tweets)
        logged_In_User.liked_tweets = liked_tweets
        logged_In_User.save()

        tweet = findTweetById(tweet_id)
        likes = tweet.likes
        likes += -1
        tweet.likes = likes
        tweet.save()
