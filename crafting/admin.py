from django.contrib import admin

from .models import DigitizingOrder, VectorOrder, PatchOrder, DigitizingOrder_Files, FinalizedDigitizingOrder, DigitizingOrderEdit, VectorOrderEdit, PatchOrderEdit
# Register your models here.


admin.site.register(DigitizingOrder)
admin.site.register(DigitizingOrder_Files)
admin.site.register(FinalizedDigitizingOrder)
admin.site.register(DigitizingOrderEdit)
admin.site.register(VectorOrderEdit)
admin.site.register(PatchOrderEdit)
admin.site.register(PatchOrder)
admin.site.register(VectorOrder)