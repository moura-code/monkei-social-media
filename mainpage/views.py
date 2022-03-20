
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect

from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse
# Create your views here.
def home(request):
    return render(request,'main/main.html')
def about(request):
    return render(request,'main/about.html')
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'main/register.html', {'form':form})

