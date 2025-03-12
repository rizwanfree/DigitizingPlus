from django.forms import forms
from .models import DigitizingOrder, DigitizingOrder_Files

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Submit

class DigitizingOrderForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(

            Row(
                Column('name', css_class='col-md-8'),
                Column('po_number', css_class='col-md-4'),
            ),
            Row(
                Column('height', css_class='col-md-4'),
                Column('width', css_class='col-md-4'),
                Column('colors', css_class='col-md-4'),
            ),
            Row(
                Column('file_format', css_class='col-md-4'),
                Column('fabric_type', css_class='col-md-4'),
                Column('logo_placement', css_class='col-md-4'),
            ),
            Row(
                Column('instruction', css_class='col-md-12'),
                
            ),
            Row(
                Column('is_urgent', css_class='col-md-6'),
                Column(Submit('submit', 'Place Order', css_class='btn btn-primary'), css_class='col-md-6'),
            ),
        )
    
    class Meta:
        model = DigitizingOrder
        fields = '__all__'
        widgets = {
            'instructions': forms.Textarea(attrs={'rows': 3})
        }



class DigitizingOrderFileForm(forms.ModelForm):
    class Meta:
        model = DigitizingOrder_Files
        fields = '__all__'
