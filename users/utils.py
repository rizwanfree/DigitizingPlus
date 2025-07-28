from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.conf import settings

def render_invoice_template(invoice, request=None):
    """Render invoice template to HTML string"""
    context = {
        'invoice': invoice,
        # Add any other context variables your template needs
    }
    return render_to_string('users/customer/invoice_email.html', context, request=request)


# utils.py
def send_invoice_email(invoice, request=None):
    """Send invoice to customer via email"""
    subject = f"Your Invoice #{invoice.invoice_number} from DigitizingPlus"
    html_content = render_invoice_template(invoice, request)
    text_content = f"Please find attached your invoice #{invoice.invoice_number}"

    email = EmailMultiAlternatives(
        subject,
        text_content,
        settings.DEFAULT_FROM_EMAIL,
        [invoice.customer.email],
        # Include secondary emails if needed
        cc=[email for email in [invoice.customer.email2, invoice.customer.email3] if email]
    )
    email.attach_alternative(html_content, "text/html")
    
    # Optionally attach PDF version if you have PDF generation
    # pdf = generate_invoice_pdf(invoice)
    # email.attach(f'invoice_{invoice.invoice_number}.pdf', pdf, 'application/pdf')
    
    email.send()



# users/utils.py
def get_effective_user(request):
    """Returns the original user if impersonating, otherwise the current user"""
    if hasattr(request, 'is_impersonating') and request.is_impersonating:
        return request.original_user  # We'll set this in the middleware
    return request.user



def send_quote_confirmation_email(quote, quote_type, request=None):
    """Send confirmation email after quote submission"""
    user = quote.user
    subject = f"Quote Confirmation - {quote_type} - {quote.name}"
    
    html_content = render_to_string('emails/quote_confirmation.html', {
        'customer_name': user.get_full_name() or user.username,
        'quote': quote,
        'quote_type': quote_type
    }, request=request)
    
    text_content = f"Thanks {user.get_full_name() or user.username}, your {quote_type} quote has been received."

    email = EmailMultiAlternatives(
        subject,
        text_content,
        settings.DEFAULT_FROM_EMAIL,
        [user.email]
    )
    email.attach_alternative(html_content, "text/html")
    email.send()