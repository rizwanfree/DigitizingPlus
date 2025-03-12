from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required

from .forms import UserRegistrationForm

from crafting.forms import DigitizingOrderFileForm

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


def log_out(request):
    logout(request)
    return redirect('web:index')


# Customer Panel Views
@login_required
def customer_dashboard(request):
    return render(request, 'users/customer/dashboard.html')


@login_required
def orders(request):
    if request.method == "POST":
        form = DigitizingOrderFileForm(request.POST)
        if form.is_valid():
            form.save()
    else:
        form = DigitizingOrderFileForm()
    return render(request, 'users/customer/orders.html', {'form': form})



# Admin Panel Views
@login_required
def admin_dashboard(request):
    return render(request, 'users/admin/dashboard.html')