from typing import Any
from django import forms
from .models import Tweet, Profile
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class TweetForm(forms.ModelForm):
    body = forms.CharField(required=True,
            widget=forms.widgets.Textarea(
                attrs={
                    "placeholder": "Enter Your Tweet",
                    "class": "form-control",
                }
            ),
            label="",      
        )
    
    class Meta:
        model = Tweet
        exclude = ("user", "likes")


class ProfilePicForm(forms.ModelForm):
    profile_image = forms.ImageField(label='profile picture')
    profile_bio = forms.CharField(label="Profile Bio", widget=forms.Textarea(attrs={'class':'form-control', 'placeholder':'Profile Bio'}))
    homepage_link = forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Website Link'}))
    facebook_link = forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Facebook Link'}))
    instagram_link = forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Instagram Link'}))
    linkedin_link = forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Linkedin Link'}))

    class Meta:
        model = Profile 
        fields = ('profile_image', 'profile_bio', 'homepage_link', 'facebook_link', 'instagram_link', 'linkedin_link')


class SignUpform(UserCreationForm):
    email = forms.EmailField(label='', widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Email address'}))
    first_name = forms.CharField(label='', max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'First name'}))
    last_name = forms.CharField(label='', max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Last name'}))

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super(SignUpform, self).__init__(*args, **kwargs)

        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['username'].widget.attrs['placeholder'] = 'User Name'
        self.fields['username'].label = ''
        self.fields['username'].help_text = '<span class="form-text text-muted"><small>Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.</small></span>'

        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['placeholder'] = 'Password'
        self.fields['password1'].label = ''
        self.fields['password1'].help_text = '<ul class="form-text text-muted small"><li>Your password can\'t be too similar to your other personal information.</li><li>Your password must contain at least 8 characters.</li><li>Your password can\'t be a commonly used password.</li><li>Your password can\'t be entirely numeric.</li></ul>'

        self.fields['password2'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['placeholder'] = 'Confirm Password'
        self.fields['password2'].label = ''
        self.fields['password2'].help_text = '<span class="form-text text-muted"><small>Enter the same password as before, for verification.</small></span>'


class UserProfileForm(UserCreationForm):
    # Exclude the 'username' field by not including it in the form
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']  # Include the fields you want to update


    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        # You can customize the form's labels, widgets, or any other properties here