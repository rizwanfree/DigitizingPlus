from django.http import Http404
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required, user_passes_test

from crafting.models import DigitizingOrder, PatchOrder, VectorOrder, DigitizingQuote, PatchQuote, VectorQuote

from .forms import UserRegistrationForm, UserProfileForm, GivenInfoForm, OptionsForm

from crafting.forms import DigitizingOrderForm, PatchOrderForm, VectorOrderForm, DigitizingQuoteForm, PatchQuoteForm, VectorQuoteForm


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
def inprocess_orders(request):
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
    return render(request, 'users/admin/inprocess-orders.html', context)


@login_required
@user_passes_test(lambda u: u.is_superuser)
def admin_order_details(request, pk, order_type):
    # Map order types to their models and templates
    ORDER_MAPPING = {
        'digitizing': {
            'model': DigitizingOrder,
            'template': 'users/admin/digitizing-order-details.html'
        },
        'patch': {
            'model': PatchOrder,
            'template': 'users/admin/patch-order-details.html'
        },
        'vector': {
            'model': VectorOrder,
            'template': 'users/admin/vector-order-details.html'
        },
    }

    # Get the correct model and template
    order_config = ORDER_MAPPING.get(order_type.lower())
    if not order_config:
        raise Http404("Invalid order type")
    
    model = order_config['model']
    my_template = order_config['template']
    
    # Get the specific order
    order = get_object_or_404(model, pk=pk)
    user = order.user

    if request.method == 'POST':
        form_type = request.POST.get('form_type')
        
        if form_type == 'given-info':
            form = GivenInfoForm(request.POST)
            if form.is_valid():
                # Update order with form data
                order.price = form.cleaned_data.get('price_option_a')
                # Update other fields as needed
                order.save()
                return redirect('success_url')
                
        elif form_type == 'final-info':
            option_form = OptionsForm(request.POST)
            if option_form.is_valid():
                # Process final info form data
                # Update order with final info if needed
                return redirect('success_url')
        else:
            # Invalid form type
            form = GivenInfoForm()
            option_form = OptionsForm()
    else:
        # Initialize forms with order data
        form = GivenInfoForm(initial={
            'design_name': order.name,
            'po_number': order.po_number,
            'width': getattr(order, 'width', ''),
            'height': getattr(order, 'height', ''),
            'colors': order.colors,
            'required_format': getattr(order, 'file_format', '') or getattr(order, 'required_format', ''),
            'placement': getattr(order, 'logo_placement', '') or getattr(order, 'patch_type', ''),
            'fabric_type': getattr(order, 'fabric_type', ''),
            'price_option_a': getattr(order, 'price', ''),
            'total_price': getattr(order, 'total_price', ''),
        })

        option_form = OptionsForm(initial={
            'width_a': getattr(order, 'width', ''),
            'height_a': getattr(order, 'height', ''),
            'stitches_a': getattr(order, 'stitches', ''),
            'price_a': getattr(order, 'price', ''),
        })

    context = {
        'order': order,
        'user': user,
        'order_type': order_type,
        'form': form,
        'final_form': option_form
    }
    return render(request, my_template, context)


@login_required
@user_passes_test(lambda u: u.is_superuser)
def admin_all_receivables(request):

    return render(request, 'users/admin/all-receivables.html')


@login_required
@user_passes_test(lambda u: u.is_superuser)
def admin_invoice_list(request):

    return render(request, 'finance/invoice-list.html')