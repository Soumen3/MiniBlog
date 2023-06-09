from django.shortcuts import render, redirect
from .forms import SignUpForm, LoginForm, PostForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from .models import Post
# Create your views here.
def home(request):
    context={}
    context['activeHome']='activate'
    posts= Post.objects.all()
    context['posts']=posts
    return render(request, 'blog/home.html', context)


def about(request):
    context={}
    context['activeAbout']='activate'
    return render(request, 'blog/about.html', context )


def contact(request):
    context={}
    context['activeContact']='activate'
    return render(request, 'blog/contact.html', context)


@login_required(login_url='Login')
def dashboard(request):
    context={}
    context['activeDashboard']='activate'
    posts= Post.objects.all()
    user=request.user
    full_name=user.get_full_name()
    grps=user.groups.all()
    context['full_name']=full_name
    context['groups']=grps
    context['posts']=posts
    return render(request, 'blog/dashboard.html', context)



def user_signup(request):
    if not request.user.is_authenticated:
        context={}
        context['activeSignup']='activate'
        if request.method == 'POST':
            form = SignUpForm(request.POST)
            if form.is_valid():
                user=form.save()
                group=Group.objects.get(name='Author')
                user.groups.add(group)
                messages.success(request, 'Congratulation! You are now an author')
                return redirect('Login')
        else:
            form=SignUpForm()
            context['form']=form
        return render(request, 'blog/signup.html', context)
    else:
        return redirect('Dashboard')


def user_login(request):
    if not request.user.is_authenticated:
        context={}
        context['activeLogin']='activate'
        if request.method == 'POST':
            form=LoginForm(request=request, data=request.POST)
            if form.is_valid():
                uname=form.cleaned_data['username']
                passw=form.cleaned_data['password']
                user=authenticate(username=uname, password=passw)
                if user is not None:
                    login(request, user)
                    messages.success(request, 'You are logged in successfully')
                    return redirect('Dashboard')
                # else:
                #     # messages.error(request, 'Invalid username or password')
                #     form=LoginForm()
        else:
            form=LoginForm()
            
        context['form']=form
        return render(request, 'blog/login.html', context)
    else:
        return redirect('Dashboard')



def user_logout(request):
    logout(request)
    messages.success(request, 'You are logged out successfully')
    return redirect('Home')


def add_post(request):
    if request.user.is_authenticated:
        context={}
        if request.method == 'POST':
            form=PostForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, 'Post added successfully')
                form=PostForm()
        else:
            form=PostForm
        context['form']=form
        return render (request, 'blog/addPost.html', context)
    else:
        return redirect('Login')


def update_post(request, id):
    if request.user.is_authenticated:
        context={}
        if request.method == 'POST':
            pi=Post.objects.get(pk=id)
            form=PostForm(request.POST, instance=pi)
            if form.is_valid():
                form.save()
                messages.success(request, 'Post updated successfully')
                return redirect('Dashboard')
        else:
            pi=Post.objects.get(pk=id)
            form=PostForm(instance=pi)
        context['form']=form
        return render (request, 'blog/updatePost.html', context)
    else:
        return redirect('Login')
    


@login_required(login_url='Login')
def delete_post(request,id):
    if request.method=='POST':
        pi=Post.objects.get(pk=id)
        pi.delete()
        messages.success(request, 'Post deleted successfully')
        return redirect('Dashboard')
        