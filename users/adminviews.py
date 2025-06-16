from email.message import EmailMessage
from django.utils import timezone
from django.http import Http404, JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.template.loader import render_to_string

from crafting.models import DigitizingOrder, FinalizedDigitizingFiles, FinalizedDigitizingOrder, FinalizedPatchFiles, FinalizedPatchOrder, FinalizedVectorFiles, FinalizedVectorOrder, PatchOrder, VectorOrder, DigitizingQuote, PatchQuote, VectorQuote
from users.models import User

from .forms import FinalDigitizingForm, UserRegistrationForm, UserProfileForm, GivenInfoForm, OptionsForm

from crafting.forms import DigitizingOrderForm, PatchOrderForm, VectorOrderForm, DigitizingQuoteForm, PatchQuoteForm, VectorQuoteForm
from django.core.mail import EmailMultiAlternatives


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
@user_passes_test(lambda u: u.is_superuser)
def inprocess_digitizing_orders(request):
    orders = DigitizingOrder.objects.select_related('user').prefetch_related('files').filter(status='Processing').order_by('-created_at')
    
    context = {
        'orders': orders,
        'order_type': 'Digitizing',
    }
    return render(request, 'users/admin/inprocess-digitizing-orders.html', context)


@login_required
@user_passes_test(lambda u: u.is_superuser)
def all_digitizing_orders(request):
    orders = DigitizingOrder.objects.select_related('user').prefetch_related('files').order_by('-created_at')
    
    context = {
        'orders': orders,
        'order_type': 'Digitizing',
    }
    return render(request, 'users/admin/all-digitizing-orders.html', context)

@login_required
@user_passes_test(lambda u: u.is_superuser)
def inprocess_patch_orders(request):
    orders = PatchOrder.objects.select_related('user').prefetch_related('files').filter(status='Processing').order_by('-created_at')
    
    context = {
        'orders': orders,
        'order_type': 'Patch',
    }
    return render(request, 'users/admin/inprocess-patch-orders.html', context)


@login_required
@user_passes_test(lambda u: u.is_superuser)
def all_patch_orders(request):
    orders = PatchOrder.objects.select_related('user').prefetch_related('files').order_by('-created_at')
    
    context = {
        'orders': orders,
        'order_type': 'Patch',
    }
    return render(request, 'users/admin/all-patch-orders.html', context)

@login_required
@user_passes_test(lambda u: u.is_superuser)
def inprocess_vector_orders(request):
    orders = VectorOrder.objects.select_related('user').prefetch_related('files').filter(status='Processing').order_by('-created_at')
    
    context = {
        'orders': orders,
        'order_type': 'Vector',
    }
    return render(request, 'users/admin/inprocess-vector-orders.html', context)


@login_required
@user_passes_test(lambda u: u.is_superuser)
def all_vector_orders(request):
    orders = VectorOrder.objects.select_related('user').prefetch_related('files').order_by('-created_at')
    
    context = {
        'orders': orders,
        'order_type': 'Vector',
    }
    return render(request, 'users/admin/all-vector-orders.html', context)



@login_required
@user_passes_test(lambda u: u.is_superuser)
def admin_order_details(request, pk, order_type):
    ORDER_MAPPING = {
        'digitizing': {
            'model': DigitizingOrder,
            'template': 'users/admin/digitizing-order-details.html',
            'final_model': FinalizedDigitizingOrder,
            'file_relation': 'digitizing_files'  # matches related_name
        },
        'patch': {
            'model': PatchOrder,
            'template': 'users/admin/patch-order-details.html',
            'final_model': FinalizedPatchOrder,
            'file_relation': 'patch_files'  # matches related_name
        },
        'vector': {
            'model': VectorOrder,
            'template': 'users/admin/vector-order-details.html',
            'final_model': FinalizedVectorOrder,
            'file_relation': 'vector_files'  # matches related_name
        },
    }

    order_config = ORDER_MAPPING.get(order_type.lower())
    if not order_config:
        raise Http404("Invalid order type")
    
    order = get_object_or_404(order_config['model'], pk=pk)
    user = order.user
    finalized_order = None
    finalized_files = []
    
    # Check if finalized version exists
    if hasattr(order, 'finalized_version'):
        finalized_order = order.finalized_version
        # Use the correct related_name from our mapping
        finalized_files = getattr(finalized_order, order_config['file_relation']).all()

    # Initialize final_form outside of POST handling
    final_form_initial = {
        'original_order': order,
        'completed_date': timezone.now().date()
    }
    if finalized_order:
        final_form_initial.update({
            'height': finalized_order.height,
            'width': finalized_order.width,
            'stitches': finalized_order.stitches,
            'price': finalized_order.price,
            'admin_notes': finalized_order.admin_notes,
            'completed_date': finalized_order.completed_date
        })
    form = GivenInfoForm()
    final_form = FinalDigitizingForm(initial=final_form_initial)

    if request.method == 'POST':
        form_type = request.POST.get('form_type')
        
        if form_type == 'given-info':
            form = GivenInfoForm(request.POST)
            if form.is_valid():
                # Update original order
                order.name = form.cleaned_data['design_name']
                order.po_number = form.cleaned_data['po_number']
                order.save()
                messages.success(request, "Order updated successfully")
                return redirect('users:admin_order_details', pk=pk, order_type=order_type)
                
        elif form_type == 'final-info':
            final_form = FinalDigitizingForm(request.POST)
            if final_form.is_valid():
                # Create or update finalized order
                finalized_order, created = order_config['final_model'].objects.update_or_create(
                    original_order=order,
                    defaults={
                        **final_form.cleaned_data,
                        'finalized_by': request.user,
                        'price': final_form.cleaned_data.get('price', 0)
                    }
                )

                # Handle file uploads
                file_mapping = {
                    'file1': 'DESIGN',
                    'file2': 'STITCH',
                    'file3': 'COLOR',
                    'file4': 'ADDITIONAL'
                }
                
                for field_name, file_type in file_mapping.items():
                    if field_name in request.FILES:
                        # Use the correct file model based on order type
                        if order_type == 'digitizing':
                            FinalizedDigitizingFiles.objects.create(
                                finalized_order=finalized_order,
                                file=request.FILES[field_name],
                                file_type=file_type
                            )
                        elif order_type == 'patch':
                            FinalizedPatchFiles.objects.create(
                                finalized_order=finalized_order,
                                file=request.FILES[field_name],
                                file_type=file_type
                            )
                        elif order_type == 'vector':
                            FinalizedVectorFiles.objects.create(
                                finalized_order=finalized_order,
                                file=request.FILES[field_name],
                                file_type=file_type
                            )

                # Create invoice if this is a new finalized order
                if created and not finalized_order.invoice:
                    finalized_order.create_invoice()

                # Send completion email if this is a new finalized order
                if created:
                    files = getattr(finalized_order, order_config['file_relation']).all()
                    send_to_emails = request.POST.getlist('send_email_to')
                    print(send_to_emails)
                    
                    if send_to_emails and files.exists():
                        # rendered HTML version
                        html_content = render_to_string('emails/order_completed.html', {
                            'order': order,
                            'user': user,
                            'order_type': order_type,
                            'finalized_order': finalized_order,
                            'finalized_files': files,
                            'site_url': request.build_absolute_uri('/')
                        })
                        
                        # fallback plain text
                        text_content = f"Your {order_type} order #{order.order_number} is ready. Please check your account for details."
                        
                        email = EmailMultiAlternatives(
                            subject=f"Your {order_type} order #{order.order_number} is ready",
                            body=text_content,
                            from_email='digitizingpluss@gmail.com',
                            to=send_to_emails,
                        )
                        email.attach_alternative(html_content, "text/html")

                        for file in files:
                            email.attach_file(file.file.path)
                                                
                        email.send()

                order.status = 'Delivered'
                order.save()
                messages.success(request, "Order finalized and email sent successfully")
                return redirect('users:admin-all-digitizing-orders')

    # Initialize form (moved after POST handling to avoid overwriting POST data)
    form = GivenInfoForm(initial={
        'design_name': order.name,
        'po_number': order.po_number,
        'height': order.height,
        'width': order.width,
        'colors': order.colors,
        'placement': order.logo_placement,
        'fabric_type': order.fabric_type
    })

    context = {
        'order': order,
        'user': user,
        'form': form,
        'final_form': final_form,
        'order_type': order_type,
        'finalized_order': finalized_order,
        'finalized_files': finalized_files
    }
    return render(request, order_config['template'], context)



@login_required
@user_passes_test(lambda u: u.is_superuser)
def update_admin_instructions(request, pk):
    order = get_object_or_404(DigitizingOrder, pk=pk)
    if request.method == 'POST':
        order.admin_instruction = request.POST.get('admin_instructions', '')
        order.save()
        return JsonResponse({
            'success': True,
            'admin_instructions': order.admin_instruction
        })
    return JsonResponse({'success': False}, status=400)



def finalize_order(request, pk):
    order = get_object_or_404(DigitizingOrder, pk=pk)
    
    if request.method == 'POST':
        form = FinalDigitizingForm(request.POST, request.FILES)
        if form.is_valid():
            finalized_order = form.save(commit=False)
            finalized_order.original_order = order
            finalized_order.finalized_by = request.user
            finalized_order.save()
            
            # Handle each file upload separately
            files = [
                ('design', form.cleaned_data.get('file1')),
                ('stitch', form.cleaned_data.get('file2')),
                ('color', form.cleaned_data.get('file3')),
                ('additional', form.cleaned_data.get('file4')),
            ]
            
            for file_type, file in files:
                if file:  # Only create records for files that were uploaded
                    FinalizedDigitizingFiles.objects.create(
                        finalized_order=finalized_order,
                        file=file,
                        description=file_type.upper()  # Or use a more descriptive label
                    )
            
            return redirect('success_url')
    else:
        form = FinalDigitizingForm(initial={
            'original_order': order.id,
            'height': order.height,
            'width': order.width,
            'completed_date': timezone.now().date()
        })
    
    return render(request, 'template.html', {'form': form})




@login_required
@user_passes_test(lambda u: u.is_superuser)
def admin_all_receivables(request):

    return render(request, 'users/admin/all-receivables.html')


@login_required
@user_passes_test(lambda u: u.is_superuser)
def admin_invoice_list(request):

    return render(request, 'finance/invoice-list.html')


# QUOTES

@login_required
@user_passes_test(lambda u: u.is_superuser)
def inprocess_digitizing_quotes(request):
    orders = DigitizingQuote.objects.select_related('user').prefetch_related('files').order_by('-created_at')
    
    context = {
        'orders': orders,
        'order_type': 'Digitizing',
    }
    return render(request, 'users/admin/inprocess-digitizing-quotes.html', context)


@login_required
@user_passes_test(lambda u: u.is_superuser)
def inprocess_vector_quotes(request):
    orders = VectorQuote.objects.select_related('user').prefetch_related('files').order_by('-created_at')
    
    context = {
        'orders': orders,
        'order_type': 'Vector',
    }
    return render(request, 'users/admin/inprocess-vector-quotes.html', context)


@login_required
@user_passes_test(lambda u: u.is_superuser)
def inprocess_patch_quotes(request):
    orders = PatchQuote.objects.select_related('user').prefetch_related('files').order_by('-created_at')
    
    context = {
        'orders': orders,
        'order_type': 'Patch',
    }
    return render(request, 'users/admin/inprocess-patch-quotes.html', context)







@login_required
@user_passes_test(lambda u: u.is_superuser)
def user_list(request):
    users = User.objects.all()
    return render(request, "users/admin/user-list.html", {"users": users})