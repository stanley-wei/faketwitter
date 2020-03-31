from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.urls import resolve
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect

import random
from .models import *
from .forms import *
from .users import *
from .tweets import *
from .database import *

def UserView(request, user_handle):
    user = findUserByHandle(user_handle)
    if user is None:
        user_exists = 'False'
        user_name = ""
        user_id = ""
        followed = 'False'
    else:
        user_exists = 'True'
        user_name = user.user_name
        user_id = user.id
        followed = checkFollow(request, user_id)
    has_Tweets = 'False'
    for tweet in Tweet.objects.all():
        if(tweet.poster.user_handle == user_handle):
            has_Tweets = 'True'
    logged_In_User = findLoggedInUser(request)
    if logged_In_User is not None:
        liked_tweets = strArrayToInt(logged_In_User.liked_tweets.split(','))
    else:
        liked_tweets = None
    bloombergAds = getBloombergAds()
    context = {
        'tweets': Tweet.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date'),
        'users': Profile.objects.all(),
        'replies': Reply.objects.all(),
        'user': user,
        'user_handle': user_handle,
        'user_name': user_name,
        'user_id': user_id,
        'user_exists': user_exists,
        'has_Tweets': has_Tweets,
        'logged_In_User': logged_In_User,
        'liked_tweets': liked_tweets,
        'followed': followed,
        'bloombergAd': 'resources/mikebloomberg/' + bloombergAds[0],
        'bloombergAdTwo': 'resources/mikebloomberg/' + bloombergAds[1]
    }
    return render(request, 'tweets/user.html', context)

def IndexView(request):
    logged_In_User = findLoggedInUser(request)
    if(logged_In_User):
        liked_tweets = strArrayToInt(logged_In_User.liked_tweets.split(','))
    else:
        liked_tweets = {''}
    bloombergAds = getBloombergAds()
    context = {
        'tweets': Tweet.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date'),
        'users': Profile.objects.all(),
        'logged_In_User': logged_In_User,
        'liked_tweets': liked_tweets,
        'bloombergAd': 'resources/mikebloomberg/' + bloombergAds[0],
        'bloombergAdTwo': 'resources/mikebloomberg/' + bloombergAds[1]
    }
    return render(request, 'tweets/index.html', context)

def FeedView(request):
    if(request.user):
        context_object_name = 'context'
        template_name = 'tweets/index.html'
        queryset = Tweet.objects.all()
        logged_In_User = findUserByHandle(request.user.username)
        followedUsers = logged_In_User.followed_users.split(',')
        followed_users = strArrayToInt(followedUsers)
        liked_tweets = strArrayToInt(logged_In_User.liked_tweets.split(','))
        bloombergAds = getBloombergAds()
        tweets_to_display = []
        has_tweets_to_display = False
        for tweet in Tweet.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date'):
            if tweet.poster.id in followed_users:
                tweets_to_display.append(tweet)
                has_tweets_to_display = True
        context = {
            'tweets': Tweet.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date'),
            'users': Profile.objects.all(),
            'logged_In_User': logged_In_User,
            'tweets_to_display': tweets_to_display,
            'has_tweets_to_display': has_tweets_to_display,
            'followed_users': followed_users,
            'liked_tweets': liked_tweets,
            'bloombergAd': 'resources/mikebloomberg/' + bloombergAds[0],
            'bloombergAdTwo': 'resources/mikebloomberg/' + bloombergAds[1]
        }
        return render(request, 'tweets/feed.html', context)
    else:
        return IndexView(request)

def RepliesView(request, user_handle, tweet_id):
    checkTweet = ''
    tweetExists = 'False'
    for tweet in Tweet.objects.all():
        if str(tweet.id) == str(tweet_id):
            checkTweet = tweet
            tweetExists = 'True'
    if user_handle == '':
        user_handle = checkTweet.poster.user_handle
    logged_In_User = findLoggedInUser(request)
    if logged_In_User is not None:
        liked_tweets = strArrayToInt(logged_In_User.liked_tweets.split(','))
    else:
        liked_tweets = {''}
    bloombergAds = getBloombergAds()
    user = findUserByHandle(user_handle)
    context = {
        'tweet': checkTweet,
        'tweet_exists': tweetExists,
        'poster': user,
        'logged_In_User': logged_In_User,
        'liked_tweets': liked_tweets,
        'bloombergAd': 'resources/mikebloomberg/' + bloombergAds[0],
        'bloombergAdTwo': 'resources/mikebloomberg/' + bloombergAds[1]
    }
    return render(request, 'tweets/replies.html', context)

def SignUpView(request):
    if(request.user):
        logout(request)
        # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = SignUpForm(request.POST, request.FILES)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            return HttpResponseRedirect('/thanks/')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = SignUpForm()
    if(request.user):
        logged_In_User = findUserByHandle(request.user.username)
    else:
        logged_In_User = None
    context = {
        'form': form,
        'has_Failed': 'False',
        'signed_Up': 'False',
        'logged_In_User': logged_In_User
    }
    return render(request, 'tweets/signup.html', context)

def LoginView(request):
        # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = LoginForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            return HttpResponseRedirect('/thanks/')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = LoginForm()
    context = {
        'form': form,
        'has_Failed': 'False',
        'logged_In': 'False'
    }
    return render(request, 'tweets/login.html', context)

@login_required(login_url='tweets/login/')
def LogoutView(request):
    logout(request)
    return render(request, 'tweets/logout.html')

def LoggingInView(request):
    if(request.user != True):
        context = attemptLogin(request.POST.get('user_handle'), request.POST.get('password'))
        if context['logged_In'] == 'True':
            user = authenticate(username = request.POST.get('user_handle'), password = request.POST.get('password'))
            login(request, user)
            logged_In_User = findLoggedInUser(request)
            context['logged_In_User'] = logged_In_User
        #return render(request, 'tweets/login.html', context)
        if context['has_Failed'] == 'False':
            return redirect(reverse('tweets:index'))
        else:
            return render(request, 'tweets/login.html', context)
    else:
        return redirect(reverse('tweets:index'))

def SigningUpView(request):
    context = signUp(request)
    logged_In_User = findLoggedInUser(request)
    context['logged_In_User'] = logged_In_User
    return render(request, 'tweets/signup.html', context)

def UpdateUserView(request):
    if(request.user):
        logged_In_User = findLoggedInUser(request)
        if request.method == 'POST':
            # create a form instance and populate it with data from the request:
            form = UpdateUserInfoForm(initial={'user_name': logged_In_User.user_name, 'password': logged_In_User.password, 'user_handle': logged_In_User.user_handle, 'profile_picture': logged_In_User.profile_picture, 'user_bio': logged_In_User.user_bio})
            # check whether it's valid:
            if form.is_valid():
                # process the data in form.cleaned_data as required
                # ...
                # redirect to a new URL:
                return HttpResponseRedirect('/thanks/')
        # if a GET (or any other method) we'll create a blank form
        else:
            form = UpdateUserInfoForm(initial={'user_name': logged_In_User.user_name, 'password': logged_In_User.password, 'user_handle': logged_In_User.user_handle, 'profile_picture': logged_In_User.profile_picture, 'user_bio': logged_In_User.user_bio})
        context = {
            'form': form,
            'has_Failed': 'False',
            'has_Updated': 'False',
            'logged_In_User': logged_In_User
        }
        return render(request, 'tweets/updateuser.html', context)
    else:no

def UpdatedUserView(request):
    updateUser(request)
    user = findLoggedInUser(request)
    login(request, user)
    context = {'logged_In_User': logged_In_User}
    return render(request, 'tweets/updateuser.html', context)

@login_required(login_url='tweets/login/')
def TweetView(request):
    form = TweetForm()
    context = {
        'form': form,
        'tweetCreated': 'False',
        'logged_In_User': findLoggedInUser(request)
    }
    return render(request, 'tweets/tweet.html', context)

@login_required(login_url='tweets/login/')
def AddTweetView(request):
    newTweet = makeNewTweet(request)
    logged_In_User = findLoggedInUser(request)
    LikeTweet(request, newTweet.id)
    context = {
        'form': TweetForm(),
        'tweetCreated': 'True',
        'logged_In_User': logged_In_User
    }
    return RepliesView(request, logged_In_User.user_handle, newTweet.id)

@login_required(login_url='tweets/login/')
def ReplyView(request, tweet_id):
    form = ReplyForm()
    foundTweet = findTweetById(tweet_id)
    logged_In_User = findLoggedInUser(request)
    context = {
        'form': form,
        'replyCreated': 'False',
        'logged_In_User': logged_In_User,
        'tweet': foundTweet,
        'liked_tweets': strArrayToInt(logged_In_User.liked_tweets.split(','))
    }
    return render(request, 'tweets/reply.html', context)

@login_required(login_url='tweets/login/')
def AddReplyView(request, tweet_id):
    logged_In_User = findLoggedInUser(request)
    newReply = Reply(tweet = findTweetById(tweet_id), reply_text = request.POST.get('reply_text'), reply_poster = logged_In_User)
    newReply.save()
    tweet = findTweetById(tweet_id)
    return RepliesView(request, tweet.poster.user_handle, tweet_id)

@login_required(login_url='tweets/login/')
def FollowUserView(request, user_handle, user_id):
    FollowUser(request, user_id)
    return redirect(reverse('tweets:user', kwargs={'user_handle':user_handle}))

@login_required(login_url='tweets/login/')
def UnfollowUserView(request, user_handle, user_id):
    UnfollowUser(request, user_id)
    return redirect(reverse('tweets:user', kwargs={'user_handle':user_handle}))

@login_required(login_url='tweets/login/')
def IndexLikeView(request, tweet_id):
    LikeTweet(request, tweet_id)
    return redirect(reverse('tweets:index'))

@login_required(login_url='tweets/login/')
def FeedLikeView(request, tweet_id):
    LikeTweet(request, tweet_id)
    return redirect(reverse('tweets:yourfeed'))

@login_required(login_url='tweets/login/')
def ReplyLikeView(request, user_handle, tweet_id):
    LikeTweet(request, int(tweet_id))
    return redirect(reverse('tweets:replies', kwargs={'user_handle': user_handle, "tweet_id":tweet_id}))

@login_required(login_url='tweets/login/')
def UserLikeView(request, user_handle, tweet_id):
    LikeTweet(request, tweet_id)
    return redirect(reverse('tweets:user', kwargs={'user_handle':user_handle}))

@login_required(login_url='tweets/login/')
def IndexUnlikeView(request, tweet_id):
    UnlikeTweet(request, tweet_id)
    return redirect(reverse('tweets:index'))

@login_required(login_url='tweets/login/')
def FeedUnlikeView(request, tweet_id):
    UnlikeTweet(request, tweet_id)
    return redirect('tweets:yourfeed')

@login_required(login_url='tweets/login/')
def ReplyUnlikeView(request, user_handle, tweet_id):
    UnlikeTweet(request, tweet_id)
    return redirect(reverse('tweets:replies', kwargs={'user_handle': user_handle, "tweet_id":tweet_id}))

@login_required(login_url='tweets/login/')
def UserUnlikeView(request, user_handle, tweet_id):
    UnlikeTweet(request, tweet_id)
    return redirect(reverse('tweets:user', kwargs={'user_handle':user_handle}))
