from datetime import date
from django.core.mail import EmailMessage
from django.conf import settings
from django.utils import timezone
from django.http import Http404, JsonResponse
from django.db.models import Sum, Max
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.template.loader import render_to_string

from crafting.models import DigitizingOrder, DigitizingOrderEdit, FinalizedDigitizingFiles, FinalizedDigitizingOrder, FinalizedPatchFiles, FinalizedVectorFiles, FinalizedVectorOrder, PatchOrder, VectorOrder, DigitizingQuote, PatchQuote, VectorQuote
from finance.models import Invoice, Payment
from frontend.models import CompanyInfo
from users.models import CreditCard, User

from .forms import FinalDigitizingForm, UserRegistrationForm, UserProfileForm, GivenInfoForm, OptionsForm

from crafting.forms import DigitizingOrderForm, PatchOrderForm, VectorOrderForm, DigitizingQuoteForm, PatchQuoteForm, VectorQuoteForm
from django.core.mail import EmailMultiAlternatives

from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import get_user_model



@login_required
@user_passes_test(lambda u: u.is_staff)
def start_impersonate(request, user_id):
    target_user = get_object_or_404(User, id=user_id)
    request.session['impersonate_id'] = target_user.id
    messages.success(request, f"Now impersonating {target_user.get_full_name()}")
    return redirect('users:customer-dashboard')

@login_required
def stop_impersonate(request):
    if 'impersonate_id' in request.session:
        del request.session['impersonate_id']
        messages.success(request, "Stopped impersonating")
    return redirect('users:admin-dashboard')  # or wherever you want to redirect after


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
def update_company_info(request):
    company = CompanyInfo.objects.first()  # Get the single instance
    
    if request.method == 'POST':
        # Update fields from POST data
        company.phone = request.POST.get('phone')
        company.email = request.POST.get('email')
        company.address = request.POST.get('address')
        company.whatsapp = request.POST.get('whatsapp')
        company.facebook = request.POST.get('facebook')
        company.instagram = request.POST.get('instagram')
        company.twitter = request.POST.get('twitter')
        company.tiktok = request.POST.get('tiktok')
        
        company.save()
        messages.success(request, 'Company information updated successfully!')
        return redirect('users:admin-dashboard')
    
    return render(request, 'users/admin/company-info.html', {'company': company})


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
    }
    return render(request, 'users/admin/inprocess-vector-orders.html', context)


@login_required
@user_passes_test(lambda u: u.is_superuser)
def all_vector_orders(request):
    orders = VectorOrder.objects.select_related('user').prefetch_related('files').order_by('-created_at')
    
    context = {
        'orders': orders,
    }
    return render(request, 'users/admin/all-vector-orders.html', context)

@login_required
@user_passes_test(lambda u: u.is_superuser)
def vector_orders_details(request, pk):
    order = get_object_or_404(VectorOrder, pk=pk)
    finalized_order = getattr(order, 'finalized_version', None)

    if request.method == 'POST':
        form_type = request.POST.get('form_type')

        if form_type == 'given-info':
            order.name = request.POST.get('name')
            order.po_number = request.POST.get('po_number')
            order.required_format = request.POST.get('required_format')
            order.color_types = request.POST.get('color_types')
            order.colors = request.POST.get('colors')
            order.others = request.POST.get('others')
            order.save()

        elif form_type == 'final-info':
            price = request.POST.get('price') or 0
            admin_notes = request.POST.get('admin_notes')
            finalized_at = request.POST.get('finalized_at') or timezone.now().date()

            finalized = finalized_order or FinalizedVectorOrder(original_order=order)
            finalized.price = price
            finalized.admin_notes = admin_notes
            finalized.finalized_at = finalized_at
            finalized.save()

            order.status = 'Delivered'
            order.save()

            file_map = {
                'vector_file': 'VECTOR',
                'source_file': 'SOURCE',
                'proof_file': 'PROOF',
                'revision_file': 'REVISION',
                'additional_file': 'ADDITIONAL',
            }

            for field_name, file_type in file_map.items():
                uploaded_file = request.FILES.get(field_name)
                if uploaded_file:
                    FinalizedVectorFiles.objects.create(
                        finalized_order=finalized,
                        file=uploaded_file,
                        file_type=file_type
                    )

                # Send email to customer
                selected_emails = request.POST.getlist('send_email_to')
                if selected_emails:
                    subject = f"Vector Order #{order.order_number} Finalized"
                    message = render_to_string('emails/order_completed.html', {
                        'order': order,
                        'finalized_order': finalized,
                        'user': order.user,
                        'order_type': 'vector'
                    })

                    email = EmailMessage(
                        subject=subject,
                        body=message,
                        from_email='digitizingpluss@gmail.com',
                        to=selected_emails
                    )
                    email.content_subtype = "html"

                    for file in finalized.vector_files.all():
                        if file.file:
                            try:
                                email.attach_file(file.file.path)
                            except Exception as e:
                                print(f"Attachment error: {e}")

                    try:
                        email.send()
                    except Exception as e:
                        print("Email send error:", e)

            return redirect('users:admin-all-vector-orders', pk=order.pk)

    vector_files = finalized_order.vector_files.all() if finalized_order else []
    file_labels = {
        'vector_file': 'Final Vector File',
        'source_file': 'Source File',
        'proof_file': 'Approval Proof',
        'revision_file': 'Revision File',
        'additional_file': 'Additional File',
    }

    return render(request, 'users/admin/vector-order-details.html', {
        'order': order,
        'user': order.user,
        'finalized_order': finalized_order,
        'vector_files': vector_files,
        'file_labels': file_labels,
    })
    return render(request, 'users/admin/all-vector-orders.html', context)



@login_required
@user_passes_test(lambda u: u.is_superuser)
def update_admin_instructions(request, pk):
    order = get_object_or_404(DigitizingOrder, pk=pk)
    if request.method == 'POST':
        order.admin_instruction = request.POST.get('admin_instructions')
        order.save()
        return JsonResponse({
            'success': True,
            'admin_instructions': order.admin_instruction
        })
    return JsonResponse({'success': False}, status=400)



@login_required
@user_passes_test(lambda u: u.is_superuser)
def finalize_digitizing_order(request, pk):
    order = get_object_or_404(DigitizingOrder, pk=pk)
    edit = order.edits.order_by('-edited_at').first()  # Get latest edit if exists
    finalized_order = getattr(order, 'finalized_version', None)

    

    # Given info is either edited version or the original
    current_info = edit if edit else order
    previous_info = order if edit else None

    print(f"Current Edited Order {current_info}")
    print(f"Previous Original Order {previous_info}")
    if request.method == 'POST':
        form_type = request.POST.get('form_type')

        if form_type == 'given-info':
            print("given-info form")
            # Always create a new edit instead of modifying original
            DigitizingOrderEdit.objects.create(
                original_order=order,
                name=request.POST.get('design_name'),
                po_number=request.POST.get('po_number'),
                width=request.POST.get('width'),
                height=request.POST.get('height'),
                colors=request.POST.get('colors'),
                logo_placement=request.POST.get('logo_placement'),
                fabric_type=request.POST.get('fabric_type')
            )

        elif form_type == 'final-info':
            finalized = finalized_order or FinalizedDigitizingOrder(original_order=order)

            finalized.width = request.POST.get('width')
            finalized.height = request.POST.get('height')
            finalized.stitches = request.POST.get('stitches') or 0
            finalized.price = request.POST.get('price') or 0
            finalized.completed_date = request.POST.get('completed_date') or timezone.now().date()
            finalized.admin_notes = request.POST.get('admin_notes')
            finalized.save()

            order.status = 'Delivered'
            order.save()

            file_map = {
                'file1': 'DESIGN',
                'file2': 'STITCH',
                'file3': 'COLOR',
                'file4': 'ADDITIONAL',
            }

            for field_name, file_type in file_map.items():
                uploaded_file = request.FILES.get(field_name)
                if uploaded_file:
                    FinalizedDigitizingFiles.objects.create(
                        finalized_order=finalized,
                        file=uploaded_file,
                        file_type=file_type
                    )

            selected_emails = request.POST.getlist('send_email_to')
            if selected_emails:
                subject = f"Digitizing Order #{order.order_number} Finalized"
                message = render_to_string('emails/order_completed.html', {
                    'order': order,
                    'finalized_order': finalized,
                    'user': order.user,
                    'order_type': 'digitizing'
                })

                email = EmailMessage(
                    subject=subject,
                    body=message,
                    from_email='digitizingpluss@gmail.com',
                    to=selected_emails
                )
                email.content_subtype = "html"

                for file in finalized.digitizing_files.all():
                    if file.file:
                        try:
                            email.attach_file(file.file.path)
                        except Exception as e:
                            print(f"Attachment error: {e}")

                try:
                    email.send()
                except Exception as e:
                    print("Email send error:", e)

            return redirect('users:admin-digitizing-details', pk=order.pk, order_type='digitizing')

    finalized_files = finalized_order.digitizing_files.all() if finalized_order else []
    today = timezone.now()

    return render(request, 'users/admin/digitizing-order-details.html', {
        'order': order,
        'user': order.user,
        'finalized_order': finalized_order,
        'finalized_files': finalized_files,
        'today': today,
        'current_info': current_info,
        'previous_info': previous_info,
    })





@login_required
@user_passes_test(lambda u: u.is_superuser)
def admin_all_receivables(request):
    users = User.objects.filter(is_superuser=False)

    data = []

    for user in users:
        invoices = Invoice.objects.filter(customer=user)
        unpaid_total = invoices.exclude(status='paid').aggregate(total_due=Sum('total'))['total_due'] or 0
        last_invoice = invoices.order_by('-date').first()
        last_payment = Payment.objects.filter(invoice__customer=user).order_by('-payment_date').first()

        data.append({
            'user': user,
            'dues': unpaid_total,
            'last_invoice_date': last_invoice.date if last_invoice else None,
            'last_invoice_status': last_invoice.status if last_invoice else 'N/A',
            'last_status_date': last_invoice.date if last_invoice else None,  # Assuming created_at == status change
            'last_payment_date': last_payment.payment_date if last_payment else None,
        })

    return render(request, 'users/admin/all-receivables.html', {"data": data})


@login_required
@user_passes_test(lambda u: u.is_superuser)
def admin_invoice_list(request):
    invoices = Invoice.objects.all()
    context = {
        'invoices': invoices
    }
    return render(request, 'finance/invoice-list.html', context)


@login_required
@user_passes_test(lambda u: u.is_superuser)
def invoice_detail(request, invoice_id):
    invoice = get_object_or_404(Invoice, id=invoice_id)
    return render(request, 'finance/invoice-detail.html', {
        'invoice': invoice
    })


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



@login_required
@user_passes_test(lambda u: u.is_superuser)
def user_detail(request, pk):
    user = get_object_or_404(User, pk=pk)

    if request.method == "POST":
        user.user_id = request.POST.get("user_id", user.user_id)
        user.email = request.POST.get("email", user.email)
        user.email2 = request.POST.get("email2", "")
        user.email3 = request.POST.get("email3", "")
        user.first_name = request.POST.get("first_name", user.first_name)
        user.last_name = request.POST.get("last_name", user.last_name)
        user.phone_number = request.POST.get("phone_number", "")
        user.address = request.POST.get("address", "")
        user.city = request.POST.get("city", "")
        user.state = request.POST.get("state", "")
        user.zip_code = request.POST.get("zip_code", "")

        try:
            user.save()
            messages.success(request, "User updated successfully.")
        except Exception as e:
            messages.error(request, f"Error updating user: {e}")

        return redirect("users:admin-user-detail", pk=pk)  # or redirect to user list

    return render(request, "users/admin/user-form.html", {"user": user})



@login_required
@user_passes_test(lambda u: u.is_superuser)
def add_credit_card(request, pk):
    user = get_object_or_404(User, pk=pk)

    # Try to fetch existing card if any
    existing_card = CreditCard.objects.filter(user=user).first()

    if request.method == 'POST':
        card_data = {
            'name_on_card': request.POST.get('name_on_card'),
            'card_number': request.POST.get('card_number'),
            'expiry_month': request.POST.get('expiry_month'),
            'expiry_year': request.POST.get('expiry_year'),
            'card_type': request.POST.get('card_type'),
            'verification_code': request.POST.get('verification_code'),
            'phone_number': request.POST.get('phone_number'),
            'email': request.POST.get('email'),
            'country': request.POST.get('country'),
            'street_address': request.POST.get('street_address'),
            'city': request.POST.get('city'),
            'state': request.POST.get('state'),
            'zip_code': request.POST.get('zip_code'),
        }

        if existing_card:
            # Update existing card
            for key, value in card_data.items():
                setattr(existing_card, key, value)
            existing_card.save()
            messages.success(request, "Credit card updated successfully.")
        else:
            # Create new card
            CreditCard.objects.create(user=user, **card_data)
            messages.success(request, "Credit card added successfully.")

        return redirect('users:admin-all-receivables')

    return render(request, 'users/admin/add-credit-card.html', {
        'user': user,
        'card': existing_card
    })



@login_required
@user_passes_test(lambda u: u.is_superuser)
def paid_invoices(request):
    invoices = Invoice.objects.filter(status='paid')
    payments = Payment.objects.all()
    return render(request, 'users/admin/paid-invoices.html', {
        'invoices': invoices,
        'title': 'Paid Invoices',
        'payments': payments
    })

@login_required
@user_passes_test(lambda u: u.is_superuser)
def unpaid_invoices(request):
    invoices = Invoice.objects.filter(status__in=['draft', 'sent', 'overdue'])
    return render(request, 'users/admin/paid-invoices.html', {  # same template reused
        'invoices': invoices,
        'title': 'Unpaid Invoices'
    })


@login_required
@user_passes_test(lambda u: u.is_superuser)
def customer_unpaid_invoices(request, user_id):
    customer = get_object_or_404(User, pk=user_id)
    unpaid_invoices = Invoice.objects.filter(customer=customer, status__in=["draft", "sent"])

    if request.method == "POST":
        invoice_ids = request.POST.getlist("invoices")
        selected_invoices = Invoice.objects.filter(id__in=invoice_ids)

        total_amount = sum(inv.total for inv in selected_invoices)

        if selected_invoices:
            subject = "Unpaid Invoices from Digitizing Plus"
            from_email = "digitizingpluss@gmail.com"
            to_email = [customer.email]

            html_content = render_to_string("emails/invoice.html", {
                "customer": customer,
                "invoices": selected_invoices,
                "total_amount": total_amount,
            })

            msg = EmailMultiAlternatives(subject, "", from_email, to_email)
            msg.attach_alternative(html_content, "text/html")
            msg.send()
            selected_invoices.update(status="sent")
            messages.success(request, "Selected invoices emailed to customer.")
        else:
            messages.warning(request, "No invoices selected.")

        return redirect("users:admin-all-receivables")

    return render(request, "users/admin/send-invoices.html", {
        "customer": customer,
        "unpaid_invoices": unpaid_invoices,
    })




@login_required
@user_passes_test(lambda u: u.is_superuser)
def manual_payment(request, invoice_id, payment_id=None):
    invoice = get_object_or_404(Invoice, pk=invoice_id)

    payment = None
    if payment_id:
        payment = get_object_or_404(Payment, pk=payment_id, invoice=invoice)

    if request.method == "POST":
        amount = request.POST.get("amount")
        method = request.POST.get("method")
        payment_date = request.POST.get("payment_date")
        note = request.POST.get("note")

        if payment:
            # Update existing payment
            payment.amount = amount
            payment.method = method
            payment.payment_date = payment_date
            payment.note = note
            payment.save()
            messages.success(request, "Payment updated successfully.")
        else:
            # Create new payment
            Payment.objects.create(
                invoice=invoice,
                amount=amount,
                method=method,
                payment_date=payment_date,
                note=note,
            )
            messages.success(request, "Payment recorded successfully.")

        return redirect("users:admin-invoice-list")

    return render(request, "users/admin/manual-payment.html", {
        "invoice": invoice,
        "payment": payment,
        "today": date.today(),
    })