from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth import login, logout
from django.contrib import messages
from .models import Blog, Profile
from django.contrib.auth.decorators import login_required
from .forms import signUpForm, ProfileForm, UserChangeProfile, BlogForm
import requests

# Create your views here.


@login_required(login_url='login')
def home(request):
    blogs = Blog.objects.filter(publish=True).order_by('-updated_at')
    return render(request, 'base/index.html', {'blogs': blogs})


def login_page(request):

    if request.user.is_authenticated:
        return redirect('home')

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
            messages.success(
                request, f'Hello {request.user.first_name} {request.user.last_name}! Welcome to Samskrut.')
            return redirect('home')
        else:
            messages.error(request, 'Username or password doesnot exist')

    return render(request, 'base/login.html')


def signup(request):

    if request.user.is_authenticated:
        return redirect('home')

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
            return redirect('profile')
        else:
            messages.error(request,
                           'Error occured while processing your request. Kindly check your credentials and try again.')

    form2 = ProfileForm(instance=profile)

    return render(request, 'base/update_profile.html', {'form1': form1, 'form2': form2})


@login_required(login_url='login')
def get_blog(request):
    response = requests.get(
        'https://wxrgxtht00.execute-api.us-east-1.amazonaws.com/getBlog')
    print(response, response.content)
    blog = response.json()
    return render(request, 'base/index.html', {'blog': blog})


def share(request, pk):
    blog = Blog.objects.get(id=pk)
    return render(request, 'base/shared_blog.html', {'blog': blog})


@login_required(login_url='login')
def add_blog(request):
    if request.method == 'POST':
        form = BlogForm(request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            form.author = request.user
            form.save()
            messages.success(request, 'Blog added successfully!')
        else:
            messages.error(
                request, 'Error occured while peocessing your request!')

    form = BlogForm()

    return render(request, 'base/add_blog.html', {'form': form})


@login_required(login_url='login')
def like(request, pk):
    blog = Blog.objects.get(id=pk)
    profile = Profile.objects.get(user=request.user)
    
    if profile not in blog.liked.all():
        blog.likes += 1
        blog.liked.add(profile)
        blog.save()
        messages.success(request, 'Liked successfully!')
    else:
        blog.likes -= 1
        blog.liked.remove(profile)
        blog.save()
        messages.success(request, 'Unliked successfully!')
    return redirect('home')


@login_required(login_url='login')
def my_blogs(request):
    blogs = Blog.objects.filter(author=request.user)
    return render(request, 'base/my_blogs.html', {'blogs': blogs})


@login_required(login_url='login')
def edit_blog(request, pk):
    blog = Blog.objects.get(id=pk)
    if request.user != blog.author:
        messages.error(
            request, 'Your not authorised to edit that blog!')
        return redirect('home')
    if request.method == 'POST':
        form = BlogForm(request.POST, instance=blog)
        if form.is_valid():
            form.save()
            messages.success(request, 'Blog update successfully!')
            return redirect('home')
        else:
            messages.error(
                request, 'Error occured while peocessing your request!')

    form = BlogForm(instance=blog)

    return render(request, 'base/edit_blog.html', {'form': form})


@login_required(login_url='login')
def publish_blog(request, pk):
    blog = Blog.objects.get(id=pk)
    if request.user != blog.author:
        messages.error(
            request, 'Your not authorised to publish that blog!')
    else:
        blog.publish = True
        blog.save()
        messages.success(request, 'Blog published successfully!')
    return redirect('my_blogs')


@login_required(login_url='login')
def unpublish_blog(request, pk):
    blog = Blog.objects.get(id=pk)
    if request.user != blog.author:
        messages.error(
            request, 'Your not authorised to unpublish that blog!')
    else:
        blog.publish = False
        blog.save()
        messages.success(request, 'Blog unpublished successfully!')
    return redirect('my_blogs')


@login_required(login_url='login')
def delete_blog(request, pk):
    blog = Blog.objects.get(id=pk)
    if request.user != blog.author:
        messages.error(
            request, 'Your not authorised to delete that blog!')
    else:
        blog.delete()
        messages.success(request, 'Blog deleted successfully!')
    return redirect('home')
