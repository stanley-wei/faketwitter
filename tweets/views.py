from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.urls import resolve
from django.contrib.auth.models import User
from .forms import SignUpForm, LoginForm, TweetForm, ReplyForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

import random
from .models import Profile, Tweet, Reply

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

def checkFollow(request, user_id):
    logged_In_User = findLoggedInUser(request)
    if(logged_In_User):
        followedusers = logged_In_User.followed_users.split(',')
        if str(user_id) in followedusers:
            return 'True'
    return 'False'

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

def getBloombergAds():
    rand = random.seed()
    randInt = random.randint(0,6)
    bloombergFiles = ['191124_vod_bloomberg_ad_hpMain_16x9_992.jpg','1573862200662.jpg','BigGayIceCream2-1200x623.jpg', 'maxresdefault (1).jpg','maxresdefault.jpg','MIKE-BLOOMBERG-AD.jpeg','unnamed.jpg']
    bloombergImageLink = bloombergFiles[randInt]
    while bloombergFiles[randInt] == bloombergImageLink:
        randInt = random.randint(0, 6)
    bloombergImageLinkTwo = bloombergFiles[randInt]
    return [bloombergImageLink, bloombergImageLinkTwo]

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
    context = attemptLogin(request.POST.get('user_handle'), request.POST.get('password'))
    if context['logged_In'] == 'True':
        user = authenticate(username = request.POST.get('user_handle'), password = request.POST.get('password'))
        login(request, user)
        logged_In_User = findLoggedInUser(request)
        context['logged_In_User'] = logged_In_User
    #return render(request, 'tweets/login.html', context)
    return IndexView(request)

def attemptLogin(user_handle, password):
    user = authenticate(username = user_handle, password = password)
    if user is None:
        context = {
            'form': LoginForm(),
            'user_name': "None",
            'has_Failed': 'True',
            'logged_In': 'False'
        }
        return context
    else:
        profile = findUserByHandle(user_handle)
        user_name = profile.user_name
        context = {
            'form': LoginForm(),
            'user_name': user_name,
            'has_Failed': 'False',
            'logged_In': 'True'
        }
        return context

def SigningUpView(request):
    context = create_new_user(request.POST.get('password'), request.POST.get('user_name'), request.POST.get('user_handle'), request.FILES.get('profile_picture'), request)
    if context['signed_Up'] == 'True':
        user = authenticate(username = request.POST.get('user_handle'), password = request.POST.get('password'))
        login(request, user)
    logged_In_User = findLoggedInUser(request)
    context['logged_In_User'] = logged_In_User
    return render(request, 'tweets/signup.html', context)

def create_new_user(password, user_name, user_handle, profile_picture, quest):
        username_Taken = 'False'
        for user in User.objects.all():
            if user.username == user_handle:
                username_Taken = 'True'
        print(profile_picture)
        if username_Taken == 'False':
            user = User.objects.create_user(user_handle)
            user.set_password(password)
            user.save()
            for foundProfile in Profile.objects.all():
                if foundProfile.user_handle == user_handle:
                    foundProfile.password = password
                    foundProfile.user_name = user_name
                    foundProfile.profile_picture = profile_picture
                foundProfile.save()
            context = {
                'user_name': user_name,
                'has_Failed': 'False',
                'signed_Up': 'True'
            }
            return context
        else:
            context = {
                'form': SignUpForm(),
                'user_name': user_name,
                'has_Failed': 'True',
                'signed_Up': 'False'
            }
            return context

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
    logged_In_User = findLoggedInUser(request)
    newTweet = Tweet(tweet_text = request.POST.get('tweet_text'), poster = logged_In_User)
    newTweet.save()
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
    return UserView(request, user_handle)

@login_required(login_url='tweets/login/')
def FollowUser(request, user_id):
    logged_In_User = findLoggedInUser(request)
    followedUsers = logged_In_User.followed_users
    logged_In_User.users_followed += 1
    followedUsers += str(user_id) + ","
    logged_In_User.followed_users = followedUsers
    user = findUserById(int(user_id))
    user.users_following += 1
    user.save()
    logged_In_User.save()

@login_required(login_url='tweets/login/')
def UnfollowUserView(request, user_handle, user_id):
    UnfollowUser(request, user_id)
    return UserView(request, user_handle)

@login_required(login_url='tweets/login/')
def UnfollowUser(request, user_id):
    logged_In_User = findLoggedInUser(request)
    followedUsers = logged_In_User.followed_users.split(',')
    logged_In_User.users_followed += -1
    while user_id in followedUsers:
        followedUsers.remove(user_id)
    followedUsers = ','.join(followedUsers)
    logged_In_User.followed_users = followedUsers
    user = findUserById(int(user_id))
    user.users_following += -1
    user.save()
    logged_In_User.save()


def findUserByHandle(user_handle):
    for user in Profile.objects.all():
        if user.user_handle == user_handle:
            return user
    return None

def findUserById(user_id):
    for profile in Profile.objects.all():
        if profile.id == user_id:
            return profile
    return None

def findTweetById(tweetId):
    for tweet in Tweet.objects.all():
        if str(tweet.id) == str(tweetId):
            return tweet
    return None

@login_required(login_url='tweets/login/')
def IndexLikeView(request, tweet_id):
    LikeTweet(request, tweet_id)
    render = IndexView(request)
    return render

@login_required(login_url='tweets/login/')
def FeedLikeView(request, tweet_id):
    LikeTweet(request, tweet_id)
    render = FeedView(request)
    return render

@login_required(login_url='tweets/login/')
def ReplyLikeView(request, user_handle, source, tweet_id):
    LikeTweet(request, int(tweet_id))
    return RepliesView(request, user_handle, int(tweet_id))

@login_required(login_url='tweets/login/')
def UserLikeView(request, user_handle, tweet_id):
    LikeTweet(request, tweet_id)
    render = UserView(request, user_handle)
    return render

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
def IndexUnlikeView(request, tweet_id):
    UnlikeTweet(request, tweet_id)
    render = IndexView(request)
    return render

@login_required(login_url='tweets/login/')
def FeedUnlikeView(request, tweet_id):
    UnlikeTweet(request, tweet_id)
    render = FeedView(request)
    return render

@login_required(login_url='tweets/login/')
def ReplyUnlikeView(request, user_handle, source, tweet_id):
    UnlikeTweet(request, tweet_id)
    render = RepliesView(request, user_handle, tweet_id)
    return render

@login_required(login_url='tweets/login/')
def UserUnlikeView(request, user_handle, tweet_id):
    UnlikeTweet(request, tweet_id)
    render = UserView(request, user_handle)
    return render

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

def findLoggedInUser(request):
    if(request.user):
        logged_In_User = findUserByHandle(request.user.username)
    else:
        logged_In_User = {'liked_tweets':''}
    return logged_In_User

def strArrayToInt(array):
    newArray = []
    for item in array:
        if item != "":
            newArray.append(int(item))
    return newArray
