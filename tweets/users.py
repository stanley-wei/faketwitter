from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

import random
from .forms import *
from .models import *
from .database import *

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

def signUp(request):
    context = create_new_user(request.POST.get('password'), request.POST.get('user_name'), request.POST.get('user_handle'), request.FILES.get('profile_picture'), request)
    if context['signed_Up'] == 'True':
        user = authenticate(username = request.POST.get('user_handle'), password = request.POST.get('password'))
        login(request, user)
    return context

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

def updateUser(request):
    logged_In_User = findLoggedInUser(request)
    logged_In_User.user_name = request.POST.get('user_name')
    logged_In_User.user_bio = request.POST.get('user_bio')
    if(request.FILES.get('profile_picture') != None):
        logged_In_User.profile_picture = request.FILES.get('profile_picture')
    logged_In_User.password = request.POST.get('password')
    logged_In_User.user_acc.set_password(request.POST.get('password'))
    logged_In_User.user_handle = request.POST.get('user_handle')
    logged_In_User.user_acc.username = request.POST.get('user_handle')

    logged_In_User.save()
    logged_In_User.user_acc.save()
    user = authenticate(username = request.POST.get('user_handle'), password = request.POST.get('password'))

def findLoggedInUser(request):
    if(request.user):
        logged_In_User = findUserByHandle(request.user.username)
    else:
        logged_In_User = {'liked_tweets':''}
    return logged_In_User

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

def checkFollow(request, user_id):
    logged_In_User = findLoggedInUser(request)
    if(logged_In_User):
        followedusers = logged_In_User.followed_users.split(',')
        if str(user_id) in followedusers:
            return 'True'
    return 'False'

def deleteUserTweets(user_id):
    for tweet in Tweet.objects.all():
        if tweet.poster.id == user_id:
            tweet.delete()

def deleteUserReplies(user_id):
    for reply in Reply.objects.all():
        if reply.reply_poster.id == user_id:
            reply.delete()
