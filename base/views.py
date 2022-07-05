from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth import login, logout
from django.contrib import messages
from .models import Profile
from django.contrib.auth.decorators import login_required
from .forms import signUpForm, ProfileForm, UserChangeProfile
import requests

# Create your views here.


@login_required(login_url='login')
def home(request):
    return render(request, 'base/index.html')


def login_page(request):

    # if request.user != None:
    #     return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'User does not exists')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Username or password doesnot exist')

    return render(request, 'base/login.html')


def signup(request):

    # if request.user != None:
    #     return redirect('home')

    form = signUpForm()

    if request.method == 'POST':
        form = signUpForm(request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            form.username = form.username.lower()
            form.save()
            messages.success(request, 'Registered Successfully! Login here.')
            return redirect('login')
        else:
            messages.error(
                request, 'Please fill the deatils correctly.')

    return render(request, 'base/signup.html', {'form': form})


@login_required(login_url='login')
def logout_user(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login')
def add_profile(request):
    form = ProfileForm()

    if request.method == 'POST':
        form = ProfileForm(request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            form.user = request.user
            form.save()
            messages.success(request, 'Profile added successfully!')
            return redirect('profile')
        else:
            messages.error(
                request, 'Error occured while processing. Kindly check your details and try again.')
            messages.warning(
                request, 'Note: The the number must be a valid 10 digit number.')

    return render(request, 'base/add_profile.html', {'form': form})


@login_required(login_url='login')
def user_profile(request):
    user = User.objects.get(username=request.user.username)
    try:
        profile = Profile.objects.get(user=request.user)
    except Exception:
        return redirect('add_profile')

    return render(request, 'base/profile.html', {'user': user, 'profile': profile})


@login_required(login_url='login')
def update_profile(request):
    form1 = UserChangeProfile(instance=request.user)
    profile = Profile.objects.get(user=request.user)

    if request.method == 'POST':
        form1 = UserChangeProfile(request.POST, instance=request.user)
        form2 = ProfileForm(request.POST, request.FILES, instance=profile)
        if all([form1.is_valid(), form2.is_valid()]):
            form1.save()
            form2.save()
            messages.success(request, 'Profile updated successfully!')
            form = ProfileForm(instance=profile)
            return redirect('profile')
        else:
            messages.error(request,
                           'Error occured while processing your request. Kindly check your credentials and try again.')

    form2 = ProfileForm(instance=profile)

    return render(request, 'base/update_profile.html', {'form1': form1, 'form2': form2})


@login_required(login_url='login')
def get_blog(request):
    response = requests.get(
        'https://7meqj4nho2.execute-api.us-east-1.amazonaws.com/getBlog')
    print(response, response.content)
    blog = response.json()
    return render(request, 'base/index.html', {'blog': blog})
