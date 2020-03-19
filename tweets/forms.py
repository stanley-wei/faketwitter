from django import forms

class SignUpForm(forms.Form):
    user_name = forms.CharField(label='Name', max_length=25)
    profile_picture = forms.ImageField(label='Profile Picture')
    user_handle = forms.CharField(label='Username', max_length=15)
    password = forms.CharField(label='Password',max_length=128)

class LoginForm(forms.Form):
    user_handle = forms.CharField(label='Username', max_length=15)
    password = forms.CharField(label='Password',max_length=128)

class TweetForm(forms.Form):
    tweet_text = forms.CharField(label='Tweet content', max_length=280, widget=forms.Textarea)

class ReplyForm(forms.Form):
    reply_text = forms.CharField(label='Reply content', max_length=280, widget=forms.Textarea)
