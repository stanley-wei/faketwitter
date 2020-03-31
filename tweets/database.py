import random
from .models import Profile, Tweet, Reply

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

def getBloombergAds():
    rand = random.seed()
    randInt = random.randint(0,6)
    bloombergFiles = ['191124_vod_bloomberg_ad_hpMain_16x9_992.jpg','1573862200662.jpg','BigGayIceCream2-1200x623.jpg', 'maxresdefault (1).jpg','maxresdefault.jpg','MIKE-BLOOMBERG-AD.jpeg','unnamed.jpg']
    bloombergImageLink = bloombergFiles[randInt]
    while bloombergFiles[randInt] == bloombergImageLink:
        randInt = random.randint(0, 6)
    bloombergImageLinkTwo = bloombergFiles[randInt]
    return [bloombergImageLink, bloombergImageLinkTwo]

def strArrayToInt(array):
    newArray = []
    for item in array:
        if item != "":
            newArray.append(int(item))
    return newArray
