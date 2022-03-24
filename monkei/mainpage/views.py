
from django.shortcuts import render, redirect
from .forms import SignUpForm, UserLoginForm

from django.contrib.auth import authenticate, login

# Create your views here.

def home(request):
    return render(request, 'main/main.html')
def about(request):
    return render(request, 'main/about.html')



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
            form = UserLoginForm(request.POST)
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

