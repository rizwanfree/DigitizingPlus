from django.contrib import admin

from .models import DigitizingOrder, DigitizingOrder_Files, FinalizedDigitizingOrder
# Register your models here.


admin.site.register(DigitizingOrder)
admin.site.register(DigitizingOrder_Files)
admin.site.register(FinalizedDigitizingOrder)