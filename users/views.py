from django.http import Http404
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required

from crafting.models import DigitizingOrder, PatchOrder, VectorOrder, DigitizingQuote, PatchQuote, VectorQuote

from .forms import UserRegistrationForm

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
def orders(request):
    print("Request method:", request.method)  # Debug print

    if request.method == 'POST':
        form_type = request.POST.get('form_type')  # Get the form type from the hidden input

        if form_type == 'digitizing':
            form = DigitizingOrderForm(request.POST, request.FILES)
        elif form_type == 'patch':
            form = PatchOrderForm(request.POST, request.FILES)
        elif form_type == 'vector':
            form = VectorOrderForm(request.POST, request.FILES)
        else:
            messages.error(request, "Invalid form submission.")
            return redirect('users:place-order')

        if form.is_valid():
            order = form.save()
            messages.success(request, f"{form_type.capitalize()} order placed successfully!")
            print("form Saved")
            return redirect('users:customer-orders-records')  # Redirect to order detail page
        else:
            messages.error(request, "Please correct the errors below.")
            print(form.errors)
    else:
        print("Something went wrong")


    # Initialize empty forms for GET requests
    digitizing_form = DigitizingOrderForm()
    patch_form = PatchOrderForm()
    vector_form = VectorOrderForm()

    context = {
        'digitizing_form': digitizing_form,
        'patch_form': patch_form,
        'vector_form': vector_form
    }
    return render(request, 'users/customer/orders.html', context)

@login_required
def order_records(request):
    # Fetch all orders from each model
    digitizing_orders = DigitizingOrder.objects.all()
    patch_orders = PatchOrder.objects.all()
    vector_orders = VectorOrder.objects.all()

    # Add a 'type' attribute to each order to identify its type
    for order in digitizing_orders:
        order.type = 'Digitizing'
    for order in patch_orders:
        order.type = 'Patch'
    for order in vector_orders:
        order.type = 'Vector'

    # Combine all orders into a single list
    all_orders = list(digitizing_orders) + list(patch_orders) + list(vector_orders)

    # Sort the combined list by creation date (or any other field)
    all_orders.sort(key=lambda x: x.created_at, reverse=True)


    context = {
        'orders': all_orders
    }
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
    if request.method == 'POST':
        form_type = request.POST.get('form_type')  # Get the form type from the hidden input

        if form_type == 'digitizing':
            form = DigitizingQuoteForm(request.POST)
        elif form_type == 'patch':
            form = PatchQuoteForm(request.POST)
        elif form_type == 'vector':
            form = VectorQuoteForm(request.POST)
        else:
            messages.error(request, "Invalid form submission.")
            return redirect('users:place-order')

        if form.is_valid():
            order = form.save()
            messages.success(request, f"{form_type.capitalize()} order placed successfully!")
            print("form Saved")
            return redirect('users:customer-quote-records')  # Redirect to order detail page
        else:
            messages.error(request, "Please correct the errors below.")
            print(form.errors)
    else:
        print("Something went wrong")


    # Initialize empty forms for GET requests
    digitizing_form = DigitizingQuoteForm()
    patch_form = PatchQuoteForm()
    vector_form = VectorQuoteForm()

    context = {
        'digitizing_form': digitizing_form,
        'patch_form': patch_form,
        'vector_form': vector_form
    }
    return render(request, 'users/customer/quotes.html', context)



@login_required
def quote_records(request):
    # Fetch all orders from each model
    digitizing_orders = DigitizingQuote.objects.all()
    patch_orders = PatchQuote.objects.all()
    vector_orders = VectorQuote.objects.all()

    # Add a 'type' attribute to each order to identify its type
    for order in digitizing_orders:
        order.type = 'Digitizing'
    for order in patch_orders:
        order.type = 'Patch'
    for order in vector_orders:
        order.type = 'Vector'

    # Combine all orders into a single list
    all_orders = list(digitizing_orders) + list(patch_orders) + list(vector_orders)

    # Sort the combined list by creation date (or any other field)
    all_orders.sort(key=lambda x: x.created_at, reverse=True)


    context = {
        'orders': all_orders
    }
    return render(request, 'users/customer/quotes-records.html', context)



# Admin Panel Views
@login_required
def admin_dashboard(request):
    return render(request, 'users/admin/dashboard.html')