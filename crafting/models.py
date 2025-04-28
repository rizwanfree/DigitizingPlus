from django.db import models
from django.conf import settings

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
    ('10% Embroidery', '100% Embroidery'),
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
    name = models.CharField(max_length=255)
    height = models.IntegerField()
    width = models.IntegerField()
    stitches = models.IntegerField(default=0)
    colors = models.IntegerField(null=True, blank=True)
    po_number = models.IntegerField(null=True, blank=True)
    file_format = models.CharField(max_length=10, choices=FORMAT_CHOICES, null=True, blank=True)
    fabric_type = models.CharField(max_length=50, choices=FABRIC_CHOICES, null=True, blank=True)
    logo_placement = models.CharField(max_length=50, choices=LOGO_PLACEMENT, null=True, blank=True)
    instructions = models.TextField(null=True, blank=True)
    is_urgent = models.BooleanField(default=False)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='Processing', blank=True)
    price = models.DecimalField(decimal_places=2, max_digits=10, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class DigitizingOrder_Files(models.Model):
    order = models.ForeignKey(DigitizingOrder, on_delete=models.CASCADE, related_name='files')
    file = models.FileField(upload_to='digitizing_order_files/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"File for Order #{self.order.name}"

class PatchOrder(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='patch_orders',
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
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='Processing', blank=True)
    price = models.DecimalField(decimal_places=2, max_digits=10, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class PatchOrder_Files(models.Model):
    order = models.ForeignKey(PatchOrder, on_delete=models.CASCADE, related_name='files')
    file = models.FileField(upload_to='patch_order_files/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"File for Order #{self.order.name}"

class VectorOrder(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='vector_orders',
    )
    name = models.CharField(max_length=255)
    po_number = models.IntegerField(null=True, blank=True)
    required_format = models.CharField(max_length=50, choices=VECTOR_ORDER_FORMAT)
    color_types = models.CharField(max_length=50, choices=VECTOR_ORDER_COLOR_TYPES)
    colors = models.IntegerField(default=1)
    others = models.CharField(max_length=255, blank=True, null=True)
    instructions = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='Processing', blank=True)
    price = models.DecimalField(decimal_places=2, max_digits=10, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class VectorOrder_Files(models.Model):
    order = models.ForeignKey(VectorOrder, on_delete=models.CASCADE, related_name='files')
    file = models.FileField(upload_to='vector_order_files/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"File for Order #{self.order.name}"

class DigitizingQuote(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='digitizing_quotes',
    )
    name = models.CharField(max_length=255)
    height = models.IntegerField()
    width = models.IntegerField()
    colors = models.IntegerField(null=True, blank=True)
    file_format = models.CharField(max_length=10, choices=FORMAT_CHOICES, null=True, blank=True)
    fabric_type = models.CharField(max_length=50, choices=FABRIC_CHOICES, null=True, blank=True)
    logo_placement = models.CharField(max_length=50, choices=LOGO_PLACEMENT, null=True, blank=True)
    instructions = models.TextField(null=True, blank=True)
    is_urgent = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class VectorQuote(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='vector_quotes',
    )
    name = models.CharField(max_length=255)
    required_format = models.CharField(max_length=50, choices=VECTOR_ORDER_FORMAT)
    color_types = models.CharField(max_length=50, choices=VECTOR_ORDER_COLOR_TYPES)
    colors = models.IntegerField(default=1)
    others = models.CharField(max_length=255, blank=True, null=True)
    instructions = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class PatchQuote(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='patch_quotes',
    )
    name = models.CharField(max_length=255)
    height = models.IntegerField()
    width = models.IntegerField()     
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
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    


class Payment(models.Model):
    PAYMENT_STATUS = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('refunded', 'Refunded'),
    ]
    
    PAYMENT_METHODS = [
        ('credit', 'Credit Card'),
        ('paypal', 'PayPal'),
        ('bank', 'Bank Transfer'),
        ('cash', 'Cash'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    transaction_id = models.CharField(max_length=100, unique=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    method = models.CharField(max_length=20, choices=PAYMENT_METHODS)
    status = models.CharField(max_length=20, choices=PAYMENT_STATUS, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"Payment #{self.transaction_id} - ${self.amount}"

class PaymentDetail(models.Model):
    payment = models.ForeignKey(Payment, related_name='details', on_delete=models.CASCADE)
    
    # Link to specific order types
    digitizing_order = models.ForeignKey(
        DigitizingOrder, 
        on_delete=models.SET_NULL, 
        null=True,
        blank=True
    )
    patch_order = models.ForeignKey(
        PatchOrder,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    vector_order = models.ForeignKey(
        VectorOrder,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def order(self):
        """Returns the associated order regardless of type"""
        return self.digitizing_order or self.patch_order or self.vector_order

    def __str__(self):
        return f"Detail for {self.payment} - {self.description}"