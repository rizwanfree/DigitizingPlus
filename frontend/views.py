from django.shortcuts import render
from django.contrib.auth import login

from users.models import User

# Create your views here.


def index(request):

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = User.objects.filter(email=email, password=password).first()

        if user is not None:
            print(user.first_name)
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
