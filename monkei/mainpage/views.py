from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from .forms import *
from .models import Post ,bananas
from django.contrib.auth import authenticate, login
from .models import Profile
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required


# Create your views here.
def about(request):
    return render(request, 'main/about.html')


def home(request,message=None):
    context = {'posts': Post.objects.all(), 'message':message }
    return render(request,'main/main.html', context=context)


def post(request):
    if not request.user.is_authenticated:
        return home(request, {'message':'You are not log in'})

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            a = Post(title=form.cleaned_data['title'].capitalize(), content=form.cleaned_data['content'], file=request.FILES['file'],image=request.FILES['image'],author=User.objects.get(id=request.user.id))
            a.save()
            bananas(id_post=a).save()

            return HttpResponseRedirect('home')
        else:
            return render(request, "main/post.html", {'form': form})
    id = request.user.id
    user= request.user
    return render(request, "main/post.html", {'form': PostForm(),'id':id,'user':user})


def register(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)

            return redirect('home')
    else:
        form = SignUpForm()

    return render(request, 'main/register.html', {'form':form})


def login_page(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == 'POST':
            form = UserLoginForm(data=request.POST)
            if form.is_valid():

                user = authenticate(
                    username=form.cleaned_data['username'],
                    password=form.cleaned_data['password'],
                )
                if user is not None:
                    login(request, user)
                    if 'next' in request.POST:
                        return redirect(request.POST['next'])
                    else:
                        return redirect('home')
        else:
            form = UserLoginForm()
        return render(request, 'main/login.html', context={'form': form})

@login_required
def profile(request):
    if request.method == 'POST':

        u_form = UserUP_form(request.POST, instance=request.user)
        p_form = ProfileUP_form(request.POST,
                                   request.FILES,
                                   instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()

            return redirect('home')

    else:
        u_form = UserUP_form(instance=request.user)
        p_form = ProfileUP_form(instance=request.user.profile)


    return render(request, 'main/profile.html', {'u_form': u_form,'p_form': p_form
    })