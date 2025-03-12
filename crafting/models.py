from django.db import models

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
    ('Cotton', 'Cotton'),
    ('Silk', 'Silk'),
    ('Wool', 'Wool'),
]

LOGO_PLACEMENT = [
    ('Left', 'Left'),
    ('Right', 'Right'),
    ('Back', 'Back'),
]

class DigitizingOrder(models.Model):
    name = models.CharField(max_length=255)
    height = models.IntegerField()
    width = models.IntegerField()
    colors = models.IntegerField(null=True, blank=True)
    po_number = models.IntegerField(null=True, blank=True)
    file_format = models.CharField(max_length=10, choices=FORMAT_CHOICES, null=True, blank=True)
    fabric_type = models.CharField(max_length=50, choices=FABRIC_CHOICES, null=True, blank=True)
    logo_placement = models.CharField(max_length=50, choices=LOGO_PLACEMENT, null=True, blank=True)
    instructions = models.TextField(null=True, blank=True)
    is_urgent = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    

class DigitizingOrder_Files(models.Model):
    order = models.ForeignKey(DigitizingOrder, on_delete=models.CASCADE, related_name='files')
    file = models.FileField(upload_to='digitizing_order_files/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"File for Order #{self.order.name}"