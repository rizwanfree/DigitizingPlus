from django.http import Http404
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required

from crafting.models import DigitizingOrder, PatchOrder, VectorOrder, DigitizingQuote, PatchQuote, VectorQuote

from .forms import UserRegistrationForm, UserProfileForm

from crafting.forms import DigitizingOrderForm, PatchOrderForm, VectorOrderForm, DigitizingQuoteForm, PatchQuoteForm, VectorQuoteForm


# Create your views here.


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        print("Submit Button pressed")
        if form.is_valid():
            user = form.save()
            print(user, 'created successfully')
            login(request, user)
            print(user, 'logged-in')
            return redirect('web:index')
        else:
            print("Form errors:", form.errors)  # Debug form errors
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
def customer_profile(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')  # Redirect to profile page after update
    else:
        form = UserProfileForm(instance=request.user)
    
    return render(request, 'users/customer/profile.html', {'form': form})


@login_required
def orders(request):
    # Initialize empty forms
    digitizing_form = DigitizingOrderForm(user=request.user)
    patch_form = PatchOrderForm(user=request.user)
    vector_form = VectorOrderForm(user=request.user)

    if request.method == 'POST':
        form_type = request.POST.get('form_type')
        
        # Handle each form type
        if form_type == 'digitizing':
            form = DigitizingOrderForm(request.POST, request.FILES, user=request.user)
        elif form_type == 'patch':
            form = PatchOrderForm(request.POST, request.FILES, user=request.user)
        elif form_type == 'vector':
            form = VectorOrderForm(request.POST, request.FILES, user=request.user)
        else:
            messages.error(request, "Invalid form submission")
            return redirect('users:place-order')

        if form.is_valid():
            form.save()
            messages.success(request, "Order placed successfully!")
            return redirect('users:customer-orders-records')
        else:
            messages.error(request, "Please fix the errors below")
            # Keep the submitted form to show errors
            if form_type == 'digitizing':
                digitizing_form = form
            elif form_type == 'patch':
                patch_form = form
            elif form_type == 'vector':
                vector_form = form

    context = {
        'digitizing_form': digitizing_form,
        'patch_form': patch_form,
        'vector_form': vector_form
    }
    return render(request, 'users/customer/orders.html', context)


@login_required
def order_records(request):
    # Get all orders for current user
    digitizing = DigitizingOrder.objects.filter(user=request.user)
    patch = PatchOrder.objects.filter(user=request.user)
    vector = VectorOrder.objects.filter(user=request.user)

    # Add type labels
    for order in digitizing:
        order.type = 'Digitizing'
    for order in patch:
        order.type = 'Patch'
    for order in vector:
        order.type = 'Vector'

    # Combine and sort by date (newest first)
    all_orders = sorted(
        list(digitizing) + list(patch) + list(vector),
        key=lambda x: x.created_at,
        reverse=True
    )

    context = {'orders': all_orders}
    return render(request, 'users/customer/records.html', context)



@login_required
def order_details(request, type, id):

    if type == 'Vector':
        obj = VectorOrder.objects.get(pk=id)
        template_name = 'users/customer/vector-order-details.html'
    elif type == 'Digitizing':
        obj = DigitizingOrder.objects.get(pk=id)
        template_name = 'users/customer/digitizing-order-details.html'
    elif type == 'Patch':
        obj = PatchOrder.objects.get(pk=id)
        template_name = 'users/customer/patch-order-details.html'
    else:
        raise Http404("Invalid order type")

    context = {
        'obj': obj
    }
    return render(request, template_name, context)



@login_required
def quotes(request):
    # Initialize empty forms
    digitizing_form = DigitizingQuoteForm(user=request.user)
    patch_form = PatchQuoteForm(user=request.user)
    vector_form = VectorQuoteForm(user=request.user)

    if request.method == 'POST':
        form_type = request.POST.get('form_type')
        
        # Handle each form type
        if form_type == 'digitizing':
            form = DigitizingQuoteForm(request.POST, user=request.user)
        elif form_type == 'patch':
            form = PatchQuoteForm(request.POST, user=request.user)
        elif form_type == 'vector':
            form = VectorQuoteForm(request.POST, user=request.user)
        else:
            messages.error(request, "Invalid form submission")
            return redirect('users:place-quote')

        if form.is_valid():
            form.save()
            messages.success(request, "Quote request submitted!")
            return redirect('users:customer-quote-records')
        else:
            messages.error(request, "Please fix the errors below")
            # Keep the submitted form to show errors
            if form_type == 'digitizing':
                digitizing_form = form
            elif form_type == 'patch':
                patch_form = form
            elif form_type == 'vector':
                vector_form = form

    context = {
        'digitizing_form': digitizing_form,
        'patch_form': patch_form,
        'vector_form': vector_form
    }
    return render(request, 'users/customer/quotes.html', context)


@login_required
def quote_records(request):
    # Get all quotes for current user
    digitizing = DigitizingQuote.objects.filter(user=request.user)
    patch = PatchQuote.objects.filter(user=request.user)
    vector = VectorQuote.objects.filter(user=request.user)

    # Add type labels
    for quote in digitizing:
        quote.type = 'Digitizing'
    for quote in patch:
        quote.type = 'Patch'
    for quote in vector:
        quote.type = 'Vector'

    # Combine and sort by date (newest first)
    all_quotes = sorted(
        list(digitizing) + list(patch) + list(vector),
        key=lambda x: x.created_at,
        reverse=True
    )

    context = {'quotes': all_quotes}
    return render(request, 'users/customer/quotes-records.html', context)




# Admin Panel Views
@login_required
def admin_dashboard(request):
    return render(request, 'users/admin/index.html')