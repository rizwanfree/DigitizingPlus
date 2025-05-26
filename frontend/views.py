from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login,authenticate

from django.core.mail import send_mail, EmailMessage
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render
from django.template.loader import render_to_string
from django.conf import settings

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
    if request.method == 'POST':
        # Get form data
        width = request.POST.get('width')
        height = request.POST.get('height')
        patch_type = request.POST.get('patch_type')
        backing = request.POST.get('backing')
        quantity = request.POST.get('quantity')
        date_needed = request.POST.get('date_needed')
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        instructions = request.POST.get('instructions')
        artwork = request.FILES.get('artwork')

        # Prepare email context
        context = {
            'width': width,
            'height': height,
            'patch_type': patch_type,
            'backing': backing,
            'quantity': quantity,
            'date_needed': date_needed,
            'name': name,
            'email': email,
            'phone': phone,
            'instructions': instructions or "None",
        }

        # Email subject
        subject = f'New Patch Quote Request from {name}'
        user_subject = 'Your Patch Quote Request Received'

        try:
            # 1. Send email to admin with attachment
            admin_message = render_to_string('frontend/emails/admin_quote_email.html', context)
            admin_email = EmailMessage(
                subject,
                admin_message,
                settings.DEFAULT_FROM_EMAIL,
                [settings.DEFAULT_FROM_EMAIL],  # Send to admin (same as from)
            )
            
            if artwork:
                admin_email.attach(artwork.name, artwork.read(), artwork.content_type)
            
            admin_email.send()

            # 2. Send confirmation email to user (plain text is fine)
            user_message = render_to_string('frontend/emails/user_quote_email.html', context)
            send_mail(
                user_subject,
                user_message,
                settings.DEFAULT_FROM_EMAIL,
                [email],
                fail_silently=False,
                html_message=user_message  # Send as HTML email
            )

            return HttpResponseRedirect(reverse('web:patches') + '?success=true')

        except Exception as e:
            print(f"Error sending emails: {e}")
            return HttpResponseRedirect(reverse('web:patches') + '?error=true')

    # For GET requests
    success = request.GET.get('success') == 'true'
    error = request.GET.get('error') == 'true'
    return render(request, "frontend/patches.html", {'success': success, 'error': error})


def faqs(request):
    return render(request, "frontend/faqs.html")

def privary_policy(request):
    return render(request, "frontend/privacy.html")

def terms(request):
    return render(request, "frontend/terms.html")