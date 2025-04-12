from django.http import Http404
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required, user_passes_test

from crafting.models import DigitizingOrder, PatchOrder, VectorOrder, DigitizingQuote, PatchQuote, VectorQuote

from .forms import UserRegistrationForm, UserProfileForm, GivenInfoForm

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
@user_passes_test(lambda u: u.is_superuser)  # Restrict to admin only
def admin_dashboard(request):
    # Get all orders with user data and prefetch files
    digitizing_orders = DigitizingOrder.objects.select_related('user').prefetch_related('files')
    patch_orders = PatchOrder.objects.select_related('user').prefetch_related('files')
    vector_orders = VectorOrder.objects.select_related('user').prefetch_related('files')

    # Combine all orders with their types
    all_orders = []
    for order in digitizing_orders:
        order.order_type = 'Digitizing'
        all_orders.append(order)
    for order in patch_orders:
        order.order_type = 'Patch'
        all_orders.append(order)
    for order in vector_orders:
        order.order_type = 'Vector'
        all_orders.append(order)

    # Sort by creation date (newest first)
    all_orders.sort(key=lambda x: x.created_at, reverse=True)

    context = {
        'orders': all_orders,
    }
    return render(request, 'users/admin/dashboard.html', context)


@login_required
@user_passes_test(lambda u: u.is_superuser)  # Restrict to admin only
def admin_order_details(request, pk, order_type):

    # Map order types to their models
    ORDER_MODELS = {
        'digitizing': DigitizingOrder,
        'patch': PatchOrder,
        'vector': VectorOrder,
    }

    # Get the correct model class
    model = ORDER_MODELS.get(order_type.lower())
    if not model:
        raise Http404("Invalid order type")
    
    # Get the specific order
    order = get_object_or_404(model, pk=pk)

    user = order.user

    if request.method == 'POST':
        form = GivenInfoForm(request.POST)
        if form.is_valid():
            # Process the data
            return redirect('success_url')
    else:
        # Initialize form with order data
        form = GivenInfoForm(initial={
            'design_name': order.name,
            'po_number': order.po_number,
            'width': getattr(order, 'width', ''),
            'height': getattr(order, 'height', ''),
            'colors': order.colors,
            'required_format': getattr(order, 'file_format', '') or getattr(order, 'required_format', ''),
            'placement': getattr(order, 'logo_placement', '') or getattr(order, 'patch_type', ''),
            'fabric_type': getattr(order, 'fabric_type', ''),
            # 'price_option_a': getattr(order, 'price_option_a', ''),
            # 'price_option_b': getattr(order, 'price_option_b', ''),
            # 'total_price': getattr(order, 'total_price', ''),
        })

    context = {
        'order': order,
        'user': user,
        'order_type': order_type,
        'form': form,
    }
    return render(request, 'users/admin/order-details.html', context)