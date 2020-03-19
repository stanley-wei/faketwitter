from django.contrib import admin

from .models import Profile, Tweet, Reply

class ReplyInline(admin.StackedInline):
    model = Reply
    extra = 0

class TweetAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['tweet_text']}),
        (None,               {'fields': ['poster']}),
        (None,               {'fields': ['likes']}),
        ('Date information', {'fields': ['pub_date']}),
    ]
    inlines = [ReplyInline]
    list_filter = ['pub_date']
    search_fields = ['tweet_text']
    search_fields = ['poster']

class UserAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['user_name']}),
        (None,               {'fields': ['profile_picture']}),
        (None, {'fields': ['user_handle']}),
        (None, {'fields': ['password']}),
        (None, {'fields': ['user_bio']}),
        (None, {'fields': ['followed_users']}),
        (None, {'fields': ['users_following']}),
        (None, {'fields': ['users_followed']}),
        (None, {'fields': ['liked_tweets']}),
        ('Date information', {'fields': ['acc_create_date']}),
    ]
    list_filter = ['acc_create_date']
    search_fields = ['user_handle']
    search_fields = ['user_name']

admin.site.register(Tweet, TweetAdmin)
admin.site.register(Profile, UserAdmin)
