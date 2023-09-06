from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Profile, Tweet
from .forms import TweetForm, SignUpform, UserProfileForm, ProfilePicForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User

def home(request):
    if request.user.is_authenticated:
        form = TweetForm(request.POST or None)
        if request.method == 'POST':
            if form.is_valid():
                tweet = form.save(commit=False)
                tweet.user = request.user
                tweet.save()
                messages.success(request, ("You tweet has been posted"))
                return redirect('home')

        tweets = Tweet.objects.all().order_by("-created_at")
        return render(request, 'home.html', {"tweets":tweets, "form":form})
    else:
        tweets = Tweet.objects.all().order_by("-created_at")
        return render(request, 'home.html', {"tweets":tweets})

def profile_list(request):
    if request.user.is_authenticated:
        profiles = Profile.objects.exclude(user=request.user)
        return render(request, 'profile_list.html', {"profiles": profiles})
    else:
        messages.success(request, ("You must be loggedin to see this page.."))
        return redirect('home')
    
def unfollow(request, pk):
    if request.user.is_authenticated:
        # get the user to unfollow
        profile = Profile.objects.get(user_id=pk)
        # unfollow the user
        request.user.profile.follows.remove(profile)
        # save the proffile
        request.user.profile.save()
        # return message
        messages.success(request, (f"You have successfully unfollow {profile.user.username}"))
        return redirect(request.META.get("HTTP_REFERER"))
    else:
        messages.success(request, ("You must be logged in to see this page."))
        return redirect('home') 
    
def follow(request, pk):
    if request.user.is_authenticated:
        # get the user to unfollow
        profile = Profile.objects.get(user_id=pk)
        # unfollow the user
        request.user.profile.follows.add(profile)
        # save the proffile
        request.user.profile.save()
        # return message
        messages.success(request, (f"You have successfully follow {profile.user.username}"))
        return redirect(request.META.get("HTTP_REFERER"))
    else:
        messages.success(request, ("You must be logged in to see this page."))
        return redirect('home') 


def profile(request, pk):
    if request.user.is_authenticated:
        profile = Profile.objects.get(user_id=pk)
        tweets = Tweet.objects.filter(user_id=pk).order_by("-created_at")
        # Post form logic
        if request.method == 'POST':
            # get current user
            current_user_profile = request.user.profile
            # get form data
            action = request.POST['follow']
            # decide to follow or unfollow
            if action == 'unfollow':
                current_user_profile.follows.remove(profile)
            elif action == 'follow':
                current_user_profile.follows.add(profile)
            # save the profile
            current_user_profile.save()

        return render(request, 'profile.html', {"profile":profile, "tweets":tweets})
    else:
        messages.success(request, ("You must be loggedin to see this page.."))

def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request,("You have been loggedin successfully! Start tweeting..."))
            return redirect('home')
        else:
            messages.success(request,('Unable to loggedin! please login again...'))
            return redirect('login')
    
    else:
        return render(request, 'login.html', {})

def logout_user(request):
    logout(request)
    messages.success(request,('You are logged out successfully..'))
    return redirect('home')

def register_user(request):
    form = SignUpform()
    if request.method == 'POST':
        form = SignUpform(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            # first_name = form.cleaned_data['first_name']
            # last_name = form.cleaned_data['last_name']
            # email = form.cleaned_data['email']
            # Log in user
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, ("You have been registered successfully. welcome!"))
            return redirect('home')

    return render(request, 'register.html', {"form":form})


def update_user(request):
    if request.user.is_authenticated:
        current_user = User.objects.get(id=request.user.id)
        profile_user = Profile.objects.get(user__id=request.user.id)

        user_form = UserProfileForm(request.POST or None, instance=current_user)
        profile_form = ProfilePicForm(request.POST or None, request.FILES or None, instance=profile_user)
        if user_form.is_valid() and profile_form.is_valid():
            print("Form is valid")
            user_form.save()
            profile_form.save()
            login(request, current_user)
            messages.success(request, ("Your profile is updated successfully."))
            return redirect('home') 
        else:
            print("User Form Errors:", user_form.errors)
            print("Profile Form Errors:", profile_form.errors)

        return render(request, 'update_user.html', {"user_form":user_form, "profile_form":profile_form})
    else:
        messages.success(request, ("You must be logged in to see this page."))
        return redirect('home') 
    
def tweet_like(request, pk):
    if request.user.is_authenticated:
        tweet = get_object_or_404(Tweet, id=pk)
        if tweet.likes.filter(id=request.user.id):
            tweet.likes.remove(request.user)
        else:
            tweet.likes.add(request.user)
        return redirect(request.META.get('HTTP_REFERER'))

    else:
        messages.success(request, ("You must be logged in to see this page."))
        return redirect('home') 
    
def tweet_show(request, pk):
    tweet = get_object_or_404(Tweet, id=pk)
    if tweet:
        return render(request, "show_tweet.html", {"tweet":tweet})
    else:
        messages.success(request, ("This tweet does not exist."))
        return redirect('home') 
