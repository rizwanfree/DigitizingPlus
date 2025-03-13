from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required

from crafting.models import DigitizingOrder, DigitizingOrder_Files

from .forms import UserRegistrationForm

from crafting.forms import DigitizingOrderForm, PatchOrderForm

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
    # if request.method == "POST":

    #     form_type = request.POST.get('form_type')

    #     # if form_type == 'digitizing':
    #     #     form = DigitizingOrderForm(request.POST, request.FILES)
    #     # if form.is_valid():
    #     #     order = form.save()
    #     #     file1 = request.FILES.get('file1')
    #     #     file2 = request.FILES.get('file2')
            
    #     #     if file1:
    #     #         DigitizingOrder_Files.objects.create(order=order,file=file1)
    #     #     if file2:
    #     #         DigitizingOrder_Files.objects.create(order=order,file=file2)
    #     #     print('Digitizing Order Save')
    # else:
    digitizing_form = DigitizingOrderForm()
    patch_form = PatchOrderForm()

    context = {
        'digitizing_form': digitizing_form,
        'patch_form': patch_form
    }
    return render(request, 'users/customer/orders.html', context)



# Admin Panel Views
@login_required
def admin_dashboard(request):
    return render(request, 'users/admin/dashboard.html')