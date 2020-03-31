from django.urls import path, re_path, reverse

from . import views

app_name = 'tweets'
urlpatterns = [
    path('', views.IndexView, name='index'),
    path('yourfeed/', views.FeedView, name='yourfeed'),

    path('user/<str:user_handle>/like/<int:tweet_id>/', views.UserLikeView, name='liketweetuser'),
    path('yourfeed/like/<str:tweet_id>', views.FeedLikeView, name='liketweetfeed'),
    path('<str:user_handle>/<str:tweet_id>/reply/liketweet/', views.ReplyLikeView, name='liketweetreply'),
    path('like/<str:tweet_id>', views.IndexLikeView, name='liketweetindex'),

    path('user/<str:user_handle>/unlike/<int:tweet_id>/', views.UserUnlikeView, name='unliketweetuser'),
    path('yourfeed/unlike/<str:tweet_id>', views.FeedUnlikeView, name='unliketweetfeed'),
    path('<str:user_handle>//<str:tweet_id>/replies/unliketweet/', views.ReplyUnlikeView, name='unliketweetreply'),
    path('unlike/<str:tweet_id>', views.IndexUnlikeView, name='unliketweetindex'),

    path('<str:user_handle>/<str:tweet_id>/replies/', views.RepliesView, name='replies'),

    path('signup/', views.SignUpView, name='signup'),
    path('signingup/', views.SigningUpView, name='signingup'),

    path('updateuser/', views.UpdateUserView, name='updateuser'),
    path('userupdated', views.UpdatedUserView, name='updateduser'),

    path('loggingin/', views.LoggingInView, name="loggingin"),
    path('login/', views.LoginView, name='login'),
    path('logout/', views.LogoutView, name='logout'),

    path('tweet/', views.TweetView, name='tweet'),
    path('addtweet/', views.AddTweetView, name='addtweet'),

    path('<str:tweet_id>/reply/', views.ReplyView, name='reply'),
    path('<str:tweet_id>/addreply/', views.AddReplyView, name='addreply'),

    path('user/<str:user_handle>/follow/<str:user_id>', views.FollowUserView, name='followuser'),
    path('<str:user_handle>/follow', views.FollowUserView, name='followuser'),
    path('user/<str:user_handle>/unfollow/<str:user_id>', views.UnfollowUserView, name='unfollowuser'),
    path('<str:user_handle>/unfollow', views.UnfollowUserView, name='unfollowuser'),

    re_path(r'^user/(?P<user_handle>\w+)/$', views.UserView, name='user'),
    re_path(r'(?P<user_handle>\w+)/$', views.UserView, name='user'),
    path('user/<str:user_handle>/', views.UserView, name='user'),
    path('<str:user_handle/', views.UserView, name='user'),
]
