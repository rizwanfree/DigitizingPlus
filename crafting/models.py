from functools import cached_property
from django.db import models
from django.conf import settings
from django.db import transaction
from django.utils import timezone

from finance.models import Invoice


# Create your models here.

FORMAT_CHOICES = [
    ('100', '100'),
    ('cnd', 'cnd'),
    ('dsb', 'dsb'),
    ('dst', 'dst'),
    ('dsz', 'dsz'),
    ('emb', 'emb'),
    ('exp', 'exp'),
    ('jef', 'jef'),
    ('ksm', 'ksm'),
    ('pes', 'pes'),
    ('pof', 'pof'),
    ('tap', 'tap'),
    ('xxx', 'xxx'),
    ('ofm', 'ofm'),
    ('pxf', 'pxf'),
    ('sus', 'sus'),
    ('hus', 'hus'),
    ('ngs', 'ngs'),
    ('Others', 'Others'),
]


FABRIC_CHOICES = [
    ('Apron', 'Apron'),
    ('Beanie', 'Beanie'),
    ('Blanket', 'Blanket'),
    ('Canvas', 'Canvas'),
    ('Chenille', 'Chenille'),
    ('Cotton Woven', 'Cotton Woven'),
    ('Denim', 'Denim'),
    ('Felt', 'Felt'),
    ('Flannel', 'Flannel'),
    ('Fleece', 'Fleece'),
    ('Knit Sweater', 'Knit Sweater'),
    ('Leather', 'Leather'),
    ('Mesh Knit', 'Mesh Knit'),
    ('Nylon', 'Nylon'),
    ('Others', 'Others'),
    ('Pique', 'Pique'),
    ('Polar Fleece', 'Polar Fleece'),
    ('Polyester', 'Polyester'),
]


LOGO_PLACEMENT = [
    ('Apron', 'Apron'),
    ('Back Applique', 'Back Applique'),
    ('Bags', 'Bags'),
    ('Beanie Caps', 'Beanie Caps'),
    ('Cap', 'Cap'),
    ('Cap Back', 'Cap Back'),
    ('Cap Puff', 'Cap Puff'),
    ('Cap Side', 'Cap Side'),
    ('Chest', 'Chest'),
    ('Chest Applique', 'Chest Applique'),
    ('Full Front Chest', 'Full Front Chest'),
    ('Gloves', 'Gloves'),
    ('Jacket Back', 'Jacket Back'),
    ('Others', 'Others'),
    ('Patches', 'Patches'),
    ('Sleeve', 'Sleeve'),
    ('Table Cloth', 'Table Cloth'),
    ('Towel', 'Towel'),
]


PATCH_TYPE = [
    ('3D Puff Patches', '3D Puff Patches'),
    ('Applique Patches', 'Applique Patches'),
    ('Blank Patches', 'Blank Patches'),
    ('Chenille Patches', 'Chenille Patches'),
    ('Embroidered Patches', 'Embroidered Patches'),
]

BORDER_TYPE = [
    ('Hot Cut Border', 'Hot Cut Border'),
    ('Merrowed Border', 'Merrowed Border'),
]


BACKING_TYPE = [
    ('Iron On (Heat Seal)', 'Iron On (Heat Seal)'),
    ('Velcro (Both Hook & Loop)', 'Velcro (Both Hook & Loop)'),
]


EMBROIDERY_FILL = [
    ('50% Embroidery', '50% Embroidery'),
    ('75% Embroidery', '75% Embroidery'),
    ('100% Embroidery', '100% Embroidery'),
]

STATUS_CHOICES = [
    ('Processing', 'Processing'),  # Order is being processed
    ('Pending', 'Pending'),        # Order is pending (optional)
    ('On Hold', 'On Hold'),        # Order is on hold (optional)
    ('Delivered', 'Delivered'),    # Order has been delivered
    ('Cancelled', 'Cancelled'),    # Order has been cancelled (optional)
]



VECTOR_ORDER_FORMAT = [
    ('cdr', 'cdr'),
    ('ai', 'ai'),
    ('eps', 'eps'),
    ('others', 'others'),
]

VECTOR_ORDER_COLOR_TYPES = [
    ('PMS', 'PMS'),
    ('RGB', 'RGB'),
    ('CMYK', 'CMYK'),
]
    #DPO = Digitizing Order
    #DPV = Vector Order
    #DPP = Patch Order

    #DPOQ = Digitizing Quote
    #DPVQ = Vector Quote
    #DPPQ = Patch Quote


class DigitizingOrder(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='digitizing_orders',
    )
    order_number = models.CharField(max_length=20, unique=True, blank=True)
    name = models.CharField(max_length=255)
    height = models.DecimalField(decimal_places=2, max_digits=10)
    width = models.DecimalField(decimal_places=2, max_digits=10)
    stitches = models.IntegerField(default=0, null=True, blank=True)
    colors = models.IntegerField(null=True, blank=True)
    po_number = models.IntegerField(null=True, blank=True)
    file_format = models.CharField(max_length=10, choices=FORMAT_CHOICES, null=True, blank=True)
    fabric_type = models.CharField(max_length=50, choices=FABRIC_CHOICES, null=True, blank=True)
    logo_placement = models.CharField(max_length=50, choices=LOGO_PLACEMENT, null=True, blank=True)
    instructions = models.TextField(null=True, blank=True)
    is_urgent = models.BooleanField(default=False)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='Processing', blank=True)
    # price = models.DecimalField(decimal_places=2, max_digits=10, blank=True, null=True)
    admin_instruction = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.order_number:
            with transaction.atomic():
                last_order = DigitizingOrder.objects.select_for_update().order_by('-id').first()
                if last_order and last_order.order_number:
                    try:
                        last_number = int(last_order.order_number[3:])  # Skip 'DO-'
                    except ValueError:
                        print(f"Invalid order_number: {last_order.order_number}")
                        last_number = 0
                else:
                    last_number = 0
                self.order_number = f"DO-{last_number + 1:04d}"
        super().save(*args, **kwargs)


class DigitizingOrderEdit(models.Model):
    original_order = models.ForeignKey(DigitizingOrder, on_delete=models.CASCADE, related_name='edits')
    order_number = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=255)
    po_number = models.CharField(max_length=50, null=True, blank=True)
    width = models.DecimalField(max_digits=6, decimal_places=2, null=True)
    height = models.DecimalField(max_digits=6, decimal_places=2, null=True)
    colors = models.IntegerField(null=True, blank=True)
    logo_placement = models.CharField(max_length=255, null=True, blank=True)
    fabric_type = models.CharField(max_length=255, null=True, blank=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='Processing', blank=True)
    edited_at = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)
    def save(self, *args, **kwargs):
        if not self.order_number:
            last_id = DigitizingOrderEdit.objects.count() + 1
            self.order_number = f"DE-{last_id:04d}"
        super().save(*args, **kwargs)

class PatchOrder(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='patch_orders',
    )
    order_number = models.CharField(max_length=20, unique=True, blank=True)
    name = models.CharField(max_length=255)
    po_number = models.IntegerField(null=True, blank=True)
    height = models.DecimalField(decimal_places=2, max_digits=5)
    width = models.DecimalField(decimal_places=2, max_digits=5)
    patch_type = models.CharField(max_length=50, choices=PATCH_TYPE, null=True, blank=True)
    backing_type = models.CharField(max_length=50, choices=BACKING_TYPE, null=True, blank=True)
    border_type = models.CharField(max_length=50, choices=BORDER_TYPE, null=True, blank=True)
    embroidery_fill = models.CharField(max_length=50, choices=EMBROIDERY_FILL, null=True, blank=True)
    quantity = models.IntegerField(default=1)
    date = models.DateField()
    color_details = models.CharField(max_length=255, blank=True, null=True)
    contact_name = models.CharField(max_length=255)
    contact_number = models.CharField(max_length=50)
    shipping_address = models.TextField(null=True, blank=True)
    instructions = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='Processing', blank=True)
    # price = models.DecimalField(decimal_places=2, max_digits=10, blank=True, null=True)
    admin_instruction = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.order_number:
            with transaction.atomic():
                # Lock the table to prevent concurrent inserts
                last_order = PatchOrder.objects.select_for_update().order_by('-id').first()
                if last_order and last_order.order_number:
                    last_number = int(last_order.order_number[2:])
                else:
                    last_number = 0
                self.order_number = f"PO-{last_number + 1:04d}"
        super().save(*args, **kwargs)
    

class PatchOrderEdit(models.Model):
    original_order = models.ForeignKey(PatchOrder, on_delete=models.CASCADE, related_name='edits')
    order_number = models.CharField(max_length=20, unique=True, blank=True)
    name = models.CharField(max_length=255)
    po_number = models.IntegerField(null=True, blank=True)
    height = models.DecimalField(decimal_places=2, max_digits=5)
    width = models.DecimalField(decimal_places=2, max_digits=5)
    patch_type = models.CharField(max_length=50, choices=PATCH_TYPE, null=True, blank=True)
    backing_type = models.CharField(max_length=50, choices=BACKING_TYPE, null=True, blank=True)
    border_type = models.CharField(max_length=50, choices=BORDER_TYPE, null=True, blank=True)
    embroidery_fill = models.CharField(max_length=50, choices=EMBROIDERY_FILL, null=True, blank=True)
    quantity = models.IntegerField(default=1)
    color_details = models.CharField(max_length=255, blank=True, null=True)
    contact_name = models.CharField(max_length=255)
    contact_number = models.CharField(max_length=50)
    shipping_address = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='Processing', blank=True)
    instructions = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    edited_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.order_number:
            last_id = PatchOrderEdit.objects.count() + 1
            self.order_number = f"PE-{last_id:04d}"
        super().save(*args, **kwargs)



class VectorOrder(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='vector_orders',
    )
    order_number = models.CharField(max_length=20, unique=True, blank=True)
    name = models.CharField(max_length=255)
    po_number = models.IntegerField(null=True, blank=True)
    required_format = models.CharField(max_length=50, choices=VECTOR_ORDER_FORMAT)
    color_types = models.CharField(max_length=50, choices=VECTOR_ORDER_COLOR_TYPES)
    colors = models.IntegerField(default=1)
    others = models.CharField(max_length=255, blank=True, null=True)
    instructions = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='Processing', blank=True)
    # price = models.DecimalField(decimal_places=2, max_digits=10, blank=True, null=True)
    admin_instruction = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.order_number:
            with transaction.atomic():
                # Lock the table to prevent concurrent inserts
                last_order = VectorOrder.objects.select_for_update().order_by('-id').first()
                if last_order and last_order.order_number:
                    last_number = int(last_order.order_number[2:])
                else:
                    last_number = 0
                self.order_number = f"VO-{last_number + 1:04d}"
        super().save(*args, **kwargs)


class VectorOrderEdit(models.Model):
    original_order = models.ForeignKey(VectorOrder, on_delete=models.CASCADE, related_name='edits')
    order_number = models.CharField(max_length=20, unique=True, blank=True)
    name = models.CharField(max_length=255)
    po_number = models.IntegerField(null=True, blank=True)
    required_format = models.CharField(max_length=50, choices=VECTOR_ORDER_FORMAT)
    color_types = models.CharField(max_length=50, choices=VECTOR_ORDER_COLOR_TYPES)
    colors = models.IntegerField(default=1)
    others = models.CharField(max_length=255, blank=True, null=True)
    instructions = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='Processing', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    edited_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.order_number:
            last_id = VectorOrderEdit.objects.count() + 1
            self.order_number = f"VE-{last_id:04d}"
        super().save(*args, **kwargs)


class DigitizingOrder_Files(models.Model):
    order = models.ForeignKey(DigitizingOrder, on_delete=models.CASCADE, related_name='files')
    file = models.FileField(upload_to='digitizing_order_files/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"File for Order #{self.order.name}"


class PatchOrder_Files(models.Model):
    order = models.ForeignKey(PatchOrder, on_delete=models.CASCADE, related_name='files')
    file = models.FileField(upload_to='patch_order_files/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"File for Order #{self.order.name}"


class VectorOrder_Files(models.Model):
    order = models.ForeignKey(VectorOrder, on_delete=models.CASCADE, related_name='files')
    file = models.FileField(upload_to='vector_order_files/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"File for Order #{self.order.name}"



### Quotes
class DigitizingQuote(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='digitizing_quotes',
    )
    name = models.CharField(max_length=255)
    height = models.DecimalField(decimal_places=2, max_digits=10)
    width = models.DecimalField(decimal_places=2, max_digits=10)
    stitches = models.IntegerField(default=0, null=True, blank=True)
    colors = models.IntegerField(null=True, blank=True)
    po_number = models.IntegerField(null=True, blank=True)
    file_format = models.CharField(max_length=10, choices=FORMAT_CHOICES, null=True, blank=True)
    fabric_type = models.CharField(max_length=50, choices=FABRIC_CHOICES, null=True, blank=True)
    logo_placement = models.CharField(max_length=50, choices=LOGO_PLACEMENT, null=True, blank=True)
    instructions = models.TextField(null=True, blank=True)
    is_urgent = models.BooleanField(default=False)
    quote_status = models.CharField(max_length=50, choices=(
        ('Requested', 'Requested'),
        ('Quoted', 'Quoted'),
        ('Accepted', 'Accepted'),
        ('Rejected', 'Rejected'),
    ), default='Requested')
    price = models.DecimalField(decimal_places=2, max_digits=10, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    converted_to_order = models.ForeignKey(
        'DigitizingOrder', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='original_quote'
    )

    def __str__(self):
        return f"Digitizing Quote - {self.name}"

    def convert_to_order(self):
        """Convert this quote to an actual order"""
        if self.converted_to_order:
            return self.converted_to_order
            
        order_data = {
            field.name: getattr(self, field.name)
            for field in DigitizingOrder._meta.fields
            if field.name not in ['id', 'order_number', 'status', 'converted_to_order']
            and hasattr(self, field.name)
        }
        
        order = DigitizingOrder.objects.create(**order_data)
        self.converted_to_order = order
        self.save()
        
        # Copy files if any
        if hasattr(self, 'files'):
            for quote_file in self.files.all():
                DigitizingOrder_Files.objects.create(
                    order=order,
                    file=quote_file.file
                )
        
        return order


class PatchQuote(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='patch_quotes',
    )
    name = models.CharField(max_length=255)
    po_number = models.IntegerField(null=True, blank=True)
    height = models.DecimalField(decimal_places=2, max_digits=5)
    width = models.DecimalField(decimal_places=2, max_digits=5)
    patch_type = models.CharField(max_length=50, choices=PATCH_TYPE, null=True, blank=True)
    backing_type = models.CharField(max_length=50, choices=BACKING_TYPE, null=True, blank=True)
    border_type = models.CharField(max_length=50, choices=BORDER_TYPE, null=True, blank=True)
    embroidery_fill = models.CharField(max_length=50, choices=EMBROIDERY_FILL, null=True, blank=True)
    quantity = models.IntegerField(default=1)
    date = models.DateField()
    color_details = models.CharField(max_length=255, blank=True, null=True)
    contact_name = models.CharField(max_length=255)
    contact_number = models.CharField(max_length=50)
    shipping_address = models.TextField(null=True, blank=True)
    instructions = models.TextField(null=True, blank=True)
    quote_status = models.CharField(max_length=50, choices=(
        ('Requested', 'Requested'),
        ('Quoted', 'Quoted'),
        ('Accepted', 'Accepted'),
        ('Rejected', 'Rejected'),
    ), default='Requested')
    price = models.DecimalField(decimal_places=2, max_digits=10, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    converted_to_order = models.ForeignKey(
        'PatchOrder', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='original_quote'
    )

    def __str__(self):
        return f"Patch Quote - {self.name}"

    def convert_to_order(self):
        """Convert this quote to an actual order"""
        if self.converted_to_order:
            return self.converted_to_order
            
        order_data = {
            field.name: getattr(self, field.name)
            for field in PatchOrder._meta.fields
            if field.name not in ['id', 'order_number', 'status', 'converted_to_order']
            and hasattr(self, field.name)
        }
        
        order = PatchOrder.objects.create(**order_data)
        self.converted_to_order = order
        self.save()
        
        # Copy files if any
        if hasattr(self, 'files'):
            for quote_file in self.files.all():
                PatchOrder_Files.objects.create(
                    order=order,
                    file=quote_file.file
                )
        
        return order


class VectorQuote(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='vector_quotes',
    )
    name = models.CharField(max_length=255)
    po_number = models.IntegerField(null=True, blank=True)
    required_format = models.CharField(max_length=50, choices=VECTOR_ORDER_FORMAT)
    color_types = models.CharField(max_length=50, choices=VECTOR_ORDER_COLOR_TYPES)
    colors = models.IntegerField(default=1)
    others = models.CharField(max_length=255, blank=True, null=True)
    instructions = models.TextField(null=True, blank=True)
    quote_status = models.CharField(max_length=50, choices=(
        ('Requested', 'Requested'),
        ('Quoted', 'Quoted'),
        ('Accepted', 'Accepted'),
        ('Rejected', 'Rejected'),
    ), default='Requested')
    price = models.DecimalField(decimal_places=2, max_digits=10, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    converted_to_order = models.ForeignKey(
        'VectorOrder', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='original_quote'
    )

    def __str__(self):
        return f"Vector Quote - {self.name}"

    def convert_to_order(self):
        """Convert this quote to an actual order"""
        if self.converted_to_order:
            return self.converted_to_order
            
        order_data = {
            field.name: getattr(self, field.name)
            for field in VectorOrder._meta.fields
            if field.name not in ['id', 'order_number', 'status', 'converted_to_order']
            and hasattr(self, field.name)
        }
        
        order = VectorOrder.objects.create(**order_data)
        self.converted_to_order = order
        self.save()
        
        # Copy files if any
        if hasattr(self, 'files'):
            for quote_file in self.files.all():
                VectorOrder_Files.objects.create(
                    order=order,
                    file=quote_file.file
                )
        
        return order


# File models for quotes
class DigitizingQuote_Files(models.Model):
    quote = models.ForeignKey(DigitizingQuote, on_delete=models.CASCADE, related_name='files')
    file = models.FileField(upload_to='digitizing_quote_files/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"File for Quote #{self.quote.name}"


class PatchQuote_Files(models.Model):
    quote = models.ForeignKey(PatchQuote, on_delete=models.CASCADE, related_name='files')
    file = models.FileField(upload_to='patch_quote_files/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"File for Quote #{self.quote.name}"


class VectorQuote_Files(models.Model):
    quote = models.ForeignKey(VectorQuote, on_delete=models.CASCADE, related_name='files')
    file = models.FileField(upload_to='vector_quote_files/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"File for Quote #{self.quote.name}"
    


class FinalizedDigitizingOrder(models.Model):
    original_order = models.OneToOneField(
        'DigitizingOrder',
        on_delete=models.CASCADE,
        related_name='finalized_version'
    )

    height = models.DecimalField(decimal_places=2, max_digits=10)
    width = models.DecimalField(decimal_places=2, max_digits=10)
    stitches = models.IntegerField(null=True, blank=True)
    price = models.DecimalField(decimal_places=2, max_digits=10)
    created_at = models.DateTimeField(auto_now_add=True)

    admin_notes = models.TextField(null=True, blank=True)
    completed_date = models.DateField()

    invoice = models.OneToOneField(
        'finance.Invoice',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='digitizing_finalization'
    )

    def create_invoice(self):
        """Create invoice only if not already linked"""
        if not self.invoice:
            invoice = Invoice.objects.create(
                customer=self.original_order.user,
                digitizing_order=self.original_order,
                total=self.price,
                status='draft'
            )
            self.invoice = invoice
            self.save(update_fields=['invoice'])

    @cached_property
    def invoice_instance(self):
        return self.invoice




class FinalizedVectorOrder(models.Model):
    original_order = models.OneToOneField(
        'VectorOrder',
        on_delete=models.CASCADE,
        related_name='finalized_version'
    )
    finalized_at = models.DateTimeField(default=timezone.now)
    price = models.DecimalField(decimal_places=2, max_digits=10)
    created_at = models.DateTimeField(auto_now_add=True)

    admin_notes = models.TextField(null=True, blank=True)
    final_files = models.FileField(upload_to='finalized/vector/', null=True, blank=True)
    revisions = models.PositiveIntegerField(default=0)

    invoice = models.OneToOneField(
        'finance.Invoice',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='vector_finalization'
    )

    def __str__(self):
        return f"Finalized Vector Order #{self.original_order.pk}"

    def create_invoice(self):
        """Create invoice only if not already attached"""
        if not self.invoice:
            invoice = Invoice.objects.create(
                customer=self.original_order.user,
                vector_order=self.original_order,
                total=self.price,
                status='draft'
            )
            self.invoice = invoice
            self.save(update_fields=['invoice'])

    @cached_property
    def invoice_instance(self):
        return self.invoice
    



class FinalizedDigitizingFiles(models.Model):
    FILE_TYPES = [
        ('DESIGN', 'Final Design File'),
        ('STITCH', 'Stitch File'),
        ('COLOR', 'Color Sheet'),
        ('ADDITIONAL', 'Additional File'),
    ]
    
    finalized_order = models.ForeignKey(
        FinalizedDigitizingOrder,
        on_delete=models.CASCADE,
        related_name='digitizing_files'
    )
    file = models.FileField(upload_to='finalized/digitizing/files/')
    file_type = models.CharField(max_length=20, choices=FILE_TYPES)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    notes = models.CharField(max_length=255, blank=True, null=True)
    
    def __str__(self):
        return f"{self.get_file_type_display()} for {self.finalized_order.order_number}"
    

class FinalizedPatchFiles(models.Model):
    FILE_TYPES = [
        ('DESIGN', 'Final Design File'),
        ('STITCH', 'Stitch File'),
        ('COLOR', 'Color Sheet'),
        ('PROOF', 'Production Proof'),
        ('ADDITIONAL', 'Additional File'),
    ]
    
    finalized_order = models.ForeignKey(
        PatchOrder,
        on_delete=models.CASCADE,
        related_name='patch_files'
    )
    file = models.FileField(upload_to='finalized/patch/files/')
    file_type = models.CharField(max_length=20, choices=FILE_TYPES)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    notes = models.CharField(max_length=255, blank=True, null=True)
    
    def __str__(self):
        return f"{self.get_file_type_display()} for {self.finalized_order.order_number}"
    

class FinalizedVectorFiles(models.Model):
    FILE_TYPES = [
        ('VECTOR', 'Final Vector File'),
        ('SOURCE', 'Source File'),
        ('PROOF', 'Approval Proof'),
        ('REVISION', 'Revision File'),
        ('ADDITIONAL', 'Additional File'),
    ]
    
    finalized_order = models.ForeignKey(
        FinalizedVectorOrder,
        on_delete=models.CASCADE,
        related_name='vector_files'
    )
    file = models.FileField(upload_to='finalized/vector/files/')
    file_type = models.CharField(max_length=20, choices=FILE_TYPES)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    notes = models.CharField(max_length=255, blank=True, null=True)
    
    def __str__(self):
        return f"{self.get_file_type_display()} for {self.finalized_order.order_number}"