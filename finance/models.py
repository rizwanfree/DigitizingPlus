from django.utils import timezone
from django.db import models
from django.conf import settings



# Create your models here.


class Invoice(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('sent', 'Sent'),
        ('paid', 'Paid'),
        ('overdue', 'Overdue'),
    ]

    # Basic info
    invoice_number = models.CharField(max_length=20, unique=True)
    customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    date = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    total = models.DecimalField(max_digits=10, decimal_places=2)

    # Use string references to avoid circular imports
    digitizing_order = models.ForeignKey(
        'crafting.DigitizingOrder', 
        on_delete=models.PROTECT, 
        null=True, 
        blank=True
    )
    patch_order = models.ForeignKey(
        'crafting.PatchOrder', 
        on_delete=models.PROTECT, 
        null=True, 
        blank=True
    )
    vector_order = models.ForeignKey(
        'crafting.VectorOrder', 
        on_delete=models.PROTECT, 
        null=True, 
        blank=True
    )

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return f"Invoice #{self.invoice_number}"

    def save(self, *args, **kwargs):
        if not self.invoice_number:
            self.invoice_number = self.generate_invoice_number()
        
        if not self.total:
            self.calculate_total()
            
        super().save(*args, **kwargs)

    def generate_invoice_number(self):
        year = timezone.now().strftime('%Y')
        last_invoice = Invoice.objects.filter(invoice_number__startswith=year).order_by('-id').first()
        if last_invoice:
            last_num = int(last_invoice.invoice_number.split('-')[-1])
            return f"{year}-{last_num + 1:04d}"
        return f"{year}-0001"

    def calculate_total(self):
        if self.digitizing_order:
            self.total = self.digitizing_order.price
        elif self.patch_order:
            self.total = self.patch_order.price
        elif self.vector_order:
            self.total = self.vector_order.price
        else:
            self.total = 0


class Payment(models.Model):
    METHOD_CHOICES = [
        ('cash', 'Cash'),
        ('card', 'Credit Card'),
        ('transfer', 'Bank Transfer'),
    ]

    invoice = models.ForeignKey(Invoice, on_delete=models.PROTECT, related_name='payments')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField(auto_now_add=True)
    method = models.CharField(max_length=20, choices=METHOD_CHOICES)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.invoice.update_status()

    def __str__(self):
        return f"Payment #{self.id} - ${self.amount}"