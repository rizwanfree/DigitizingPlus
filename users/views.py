from django.shortcuts import render, redirect
from django.contrib.auth import login

from .forms import UserRegistrationForm

# Create your views here.


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            print(user, 'created successfully')
            login(request, user)
            print(user, 'logged-in')
            return redirect('web:index')
        
    else:
        form = UserRegistrationForm()
    return render(request, 'registration/register.html', {'form': form})