from django.utils import timezone
from django.http import Http404
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import update_session_auth_hash
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from crafting.models import DigitizingOrder, PatchOrder, VectorOrder, DigitizingQuote, PatchQuote, VectorQuote, VectorQuote_Files, DigitizingQuote_Files, PatchQuote_Files, DigitizingOrder_Files, VectorOrder_Files, PatchOrder_Files
from finance.models import Invoice

from .forms import FinalDigitizingForm, UserRegistrationForm, UserProfileForm, GivenInfoForm, OptionsForm

from crafting.forms import DigitizingOrderForm, PatchOrderForm, VectorOrderForm, DigitizingQuoteForm, PatchQuoteForm, VectorQuoteForm

from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags


# Create your views here.


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        print("Submit Button pressed")
        if form.is_valid():
            user = form.save(commit=False)  # Don't save yet
            raw_password = form.cleaned_data.get('password1')  # Get plain password
            user.set_password(raw_password)  # Now hash it
            user.save()
            print(user, 'created successfully')
            
            # Send welcome email
            try:
                subject = 'Welcome to DigitizingPlus'
                html_message = render_to_string('emails/register.html', {
                    'user': user,
                    'raw_password': raw_password,  # Passing plain password to template
                })
                plain_message = strip_tags(html_message)
                from_email = settings.DEFAULT_FROM_EMAIL
                to_email = user.email
                
                send_mail(
                    subject,
                    plain_message,
                    from_email,
                    [to_email],
                    html_message=html_message,
                    fail_silently=False,
                )
                print(f"Welcome email sent to {user.email}")
            except Exception as e:
                print(f"Failed to send welcome email: {str(e)}")
            
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
            user = form.save(commit=False)
            password_changed = False
            
            # Handle password change
            current_password = form.cleaned_data.get('current_password')
            new_password = form.cleaned_data.get('new_password')
            confirm_password = form.cleaned_data.get('confirm_password')
            
            if new_password:
                if not request.user.check_password(current_password):
                    form.add_error('current_password', 'Current password is incorrect')
                    return render(request, 'users/customer/profile.html', {'form': form})
                
                if new_password != confirm_password:
                    form.add_error('confirm_password', 'New passwords do not match')
                    return render(request, 'users/customer/profile.html', {'form': form})
                
                user.set_password(new_password)
                password_changed = True
            
            user.save()
            
            # Send profile update email
            try:
                context = {
                    'user': user,
                    'site_name': 'Your Site Name',
                    'timestamp': timezone.now(),
                    'password_changed': password_changed
                }
                
                subject = 'Your Profile Has Been Updated'
                html_message = render_to_string('emails/profile_update.html', context)
                plain_message = strip_tags(html_message)
                
                send_mail(
                    subject,
                    plain_message,
                    settings.DEFAULT_FROM_EMAIL,
                    [user.email],
                    html_message=html_message,
                    fail_silently=False
                )
            except Exception as e:
                # Log error but don't interrupt user flow
                print(f"Failed to send profile update email: {e}")
            
            messages.success(request, 'Profile updated successfully!')
            
            if password_changed:
                update_session_auth_hash(request, user)
                messages.info(request, 'Your password has been updated')
            
            return redirect('users:customer-dashboard')
    else:
        form = UserProfileForm(instance=request.user)
    
    return render(request, 'users/customer/profile.html', {'form': form})


@login_required
def orders(request):
    digitizing_form = DigitizingOrderForm(user=request.user)
    patch_form = PatchOrderForm(user=request.user)
    vector_form = VectorOrderForm(user=request.user)

    if request.method == 'POST':
        form_type = request.POST.get('form_type')
        
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
            order = form.save()
            
            # Prepare email context
            context = {
                'order_number': order.order_number,
                'customer_name': request.user.get_full_name(),
                'order_details': order,
                'order_type': form_type.capitalize()
            }
            
            # 1. Send confirmation to customer
            subject_customer = f"Order Confirmation #{order.id}"
            html_content_customer = render_to_string('emails/order_confirmation.html', context)
            text_content_customer = strip_tags(html_content_customer)
            
            email_customer = EmailMultiAlternatives(
                subject_customer,
                text_content_customer,
                'digitizingplus@gmail.com',
                [request.user.email]
            )
            email_customer.attach_alternative(html_content_customer, "text/html")
            email_customer.send()
            
            # 2. Send notification to admin
            subject_admin = f"New {form_type} Order Received (#{order.order_number})"
            html_content_admin = render_to_string('emails/admin_order_notification.html', context)
            text_content_admin = strip_tags(html_content_admin)
            
            email_admin = EmailMultiAlternatives(
                subject_admin,
                text_content_admin,
                'digitizingplus@gmail.com',
                ['admin@digitizingplus.com']  # Replace with admin email
            )
            email_admin.attach_alternative(html_content_admin, "text/html")
            email_admin.send()
            
            messages.success(request, "Order placed successfully! Check your email for confirmation.")
            return redirect('users:customer-orders-records')
        
        else:
            messages.error(request, "Please fix the errors below")
            if form_type == 'digitizing':
                digitizing_form = form
            elif form_type == 'patch':
                patch_form = form
            elif form_type == 'vector':
                vector_form = form

    context = {
        'digitizing_form': digitizing_form,
        'patch_form': patch_form,
        'vector_form': vector_form,
        'edit_mode': False
    }
    return render(request, 'users/customer/orders.html', context)



@login_required
def edit_order(request, type, id):
    # Get the order object
    if type == 'Vector':
        order = get_object_or_404(VectorOrder, pk=id, user=request.user)
        form_class = VectorOrderForm
        file_model = VectorOrder_Files
        active_tab = 'vector'
    elif type == 'Digitizing':
        order = get_object_or_404(DigitizingOrder, pk=id, user=request.user)
        form_class = DigitizingOrderForm
        file_model = DigitizingOrder_Files
        active_tab = 'digitizing'
    elif type == 'Patch':
        order = get_object_or_404(PatchOrder, pk=id, user=request.user)
        form_class = PatchOrderForm
        file_model = PatchOrder_Files
        active_tab = 'patch'
    else:
        raise Http404("Invalid order type")

    if request.method == 'POST':
        form = form_class(request.POST, request.FILES, instance=order, user=request.user)
        if form.is_valid():
            order = form.save()
            
            # Handle file updates
            file1 = form.cleaned_data.get('file1')
            file2 = form.cleaned_data.get('file2')
            
            # Clear existing files if new ones are uploaded
            if file1 or file2:
                file_model.objects.filter(order=order).delete()
                
            if file1:
                file_model.objects.create(order=order, file=file1)
            if file2:
                file_model.objects.create(order=order, file=file2)
                
            messages.success(request, "Order updated successfully!")
            return redirect('users:customer-order-details', type=type, id=id)
    else:
        form = form_class(instance=order, user=request.user)
        # Get existing files to display in the form
        existing_files = file_model.objects.filter(order=order)
        if existing_files.exists():
            form.fields['file1'].help_text = f"Current file: {existing_files.first().file.name}"
            if existing_files.count() > 1:
                form.fields['file2'].help_text = f"Current file: {existing_files[1].file.name}"

    # Create empty forms for other tabs
    forms = {
        'digitizing_form': DigitizingOrderForm(user=request.user) if active_tab != 'digitizing' else form,
        'patch_form': PatchOrderForm(user=request.user) if active_tab != 'patch' else form,
        'vector_form': VectorOrderForm(user=request.user) if active_tab != 'vector' else form,
    }

    context = {
        'edit_mode': True,
        'active_tab': active_tab,
        'type': type,
        'order_id': id,
        **forms
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
        order = VectorOrder.objects.get(pk=id)
        template_name = 'users/customer/vector-order-details.html'
    elif type == 'Digitizing':
        order = DigitizingOrder.objects.get(pk=id)
        template_name = 'users/customer/digitizing-order-details.html'
    elif type == 'Patch':
        order = PatchOrder.objects.get(pk=id)
        template_name = 'users/customer/patch-order-details.html'
    else:
        raise Http404("Invalid order type")

    context = {
        'order': order,
        'type': type
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

    # Add type labels and convert to list of dicts for easier processing
    all_quotes = []
    
    for quote in digitizing:
        quote.type = 'Digitizing'
        all_quotes.append(quote)
    
    for quote in patch:
        quote.type = 'Patch'
        all_quotes.append(quote)
    
    for quote in vector:
        quote.type = 'Vector'
        all_quotes.append(quote)

    # Sort by created_at (newest first)
    all_quotes.sort(key=lambda x: x.created_at, reverse=True)

    context = {'quotes': all_quotes}
    return render(request, 'users/customer/quotes-records.html', context)


@login_required
def digitizing_quote_details(request, pk):
    try:
        quote = DigitizingQuote.objects.get(pk=pk, user=request.user)
        files = DigitizingQuote_Files.objects.filter(quote=quote)
        
        context = {
            'quote': quote,
            'files': files,
            'can_accept': quote.quote_status == 'Quoted' and not quote.converted_to_order
        }
        return render(request, 'users/customer/digitizing-quote-details.html', context)
    
    except DigitizingQuote.DoesNotExist:
        raise Http404("Quote not found or you don't have permission to view it")


@login_required
def patch_quote_details(request, pk):
    try:
        quote = PatchQuote.objects.get(pk=pk, user=request.user)
        files = PatchQuote_Files.objects.filter(quote=quote)
        
        context = {
            'quote': quote,
            'files': files,
            'can_accept': quote.quote_status == 'Quoted' and not quote.converted_to_order
        }
        return render(request, 'users/customer/patch-quote-details.html', context)
    
    except PatchQuote.DoesNotExist:
        raise Http404("Quote not found or you don't have permission to view it")


@login_required
def vector_quote_details(request, pk):
    try:
        quote = VectorQuote.objects.get(pk=pk, user=request.user)
        files = VectorQuote_Files.objects.filter(quote=quote)
        
        context = {
            'quote': quote,
            'files': files,
            'can_accept': quote.quote_status == 'Quoted' and not quote.converted_to_order
        }
        return render(request, 'users/customer/vector-quote-details.html', context)
    
    except VectorQuote.DoesNotExist:
        raise Http404("Quote not found or you don't have permission to view it")


@login_required
def accept_quote(request, quote_type, pk):
    try:
        if quote_type == 'digitizing':
            quote = DigitizingQuote.objects.get(pk=pk, user=request.user)
            order = quote.convert_to_order()
            messages.success(request, 'Quote accepted and converted to order successfully!')
            return redirect('digitizing-order-details', pk=order.id)
            
        elif quote_type == 'patch':
            quote = PatchQuote.objects.get(pk=pk, user=request.user)
            order = quote.convert_to_order()
            messages.success(request, 'Quote accepted and converted to order successfully!')
            return redirect('patch-order-details', pk=order.id)
            
        elif quote_type == 'vector':
            quote = VectorQuote.objects.get(pk=pk, user=request.user)
            order = quote.convert_to_order()
            messages.success(request, 'Quote accepted and converted to order successfully!')
            return redirect('vector-order-details', pk=order.id)
            
    except (DigitizingQuote.DoesNotExist, PatchQuote.DoesNotExist, VectorQuote.DoesNotExist):
        raise Http404("Quote not found or you don't have permission to accept it")
    except Exception as e:
        messages.error(request, f'Error accepting quote: {str(e)}')
        return redirect('quote-records')



# Invoices Views

@login_required
def invoice_list(request):
    """
    Show all invoices for the logged-in user with order type
    """
    invoices = Invoice.objects.filter(customer=request.user).order_by('-created_at')
    
    # Add order type to each invoice
    for invoice in invoices:
        if invoice.digitizing_order:
            invoice.order_type = "Digitizing"
            invoice.order = invoice.digitizing_order
        elif invoice.patch_order:
            invoice.order_type = "Patch"
            invoice.order = invoice.patch_order
        elif invoice.vector_order:
            invoice.order_type = "Vector"
            invoice.order = invoice.vector_order
        else:
            invoice.order_type = "Unknown"
            
    
    return render(request, 'users/customer/invoice_list.html', {
        'invoices': invoices
    })


@login_required
def invoice_detail(request, invoice_id):
    """
    Simple view to show details of one invoice
    """
    # Get the invoice or show 404 error
    invoice = get_object_or_404(Invoice, id=invoice_id, customer=request.user)
    user = invoice.customer
    if invoice.digitizing_order:
        invoice.order_type = "Digitizing"
        invoice.order = invoice.digitizing_order
    elif invoice.patch_order:
        invoice.order_type = "Patch"
        invoice.order = invoice.patch_order
    elif invoice.vector_order:
        invoice.order_type = "Vector"
        invoice.order = invoice.vector_order
    else:
            invoice.order_type = "Unknown"
    
    return render(request, 'users/customer/invoice_detail.html', {
        'invoice': invoice,
        'user': user
    })

