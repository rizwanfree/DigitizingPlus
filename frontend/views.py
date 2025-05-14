from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login,authenticate

from users.models import User

# Create your views here.


def index(request):

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(request, user_id=email, password=password)

        if user is not None:
            login(request, user)
            if user.is_staff:
                return redirect('users:admin-dashboard')
            else:
                return redirect('users:customer-dashboard')
            
        else:
            print("Invalid User")

    return render(request, "frontend/index.html")

def features(request):
    return render(request, "frontend/features.html")

def services(request):
    return render(request, "frontend/services.html")

def portfolio(request):
    return render(request, "frontend/portfolio.html")

def pricing(request):
    return render(request, "frontend/pricing.html")

def payment(request):
    return render(request, "frontend/payment.html")

def contact(request):
    return render(request, "frontend/contact.html")

def vector(request):
    return render(request, "frontend/vector.html")

def patches(request):
    return render(request, "frontend/patches.html")


def faqs(request):
    return render(request, "frontend/faqs.html")

def privary_policy(request):
    return render(request, "frontend/privacy.html")

def terms(request):
    return render(request, "frontend/terms.html")