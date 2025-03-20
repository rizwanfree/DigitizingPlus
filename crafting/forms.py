from django import forms
from django.core.exceptions import ValidationError
from .models import DigitizingOrder, PatchOrder, VectorOrder, DigitizingOrder_Files, PatchOrder_Files, VectorOrder_Files, DigitizingQuote, PatchQuote, VectorQuote

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Submit, Reset, HTML

class DigitizingOrderForm(forms.ModelForm):

    file1 = forms.FileField(label='Upload Files (2 MB Max Size)', required=False)
    file2 = forms.FileField(label='', required=False)

    def clean_file1(self):
        file1 = self.cleaned_data.get('file1')
        if file1:
            if file1.size > 2 * 1024 * 1024:  # 2 MB limit
                raise ValidationError("File 1 must be less than 2 MB.")
        return file1

    def clean_file2(self):
        file2 = self.cleaned_data.get('file2')
        if file2:
            if file2.size > 2 * 1024 * 1024:  # 2 MB limit
                raise ValidationError("File 2 must be less than 2 MB.")
        return file2

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
                Column('instructions', css_class='col-md-6'),
                Column(Row(
                    Column('file1', css_class='col-md-12'),
                    Column('file2', css_class='col-md-12 mt-0'),  
                ), css_class='col-md-6'),                
            ),
            Row(
                Column('is_urgent', css_class='col-md-8'),
                Column(Submit('submit', 'Place Order', css_class='btn btn-primary w-100'), css_class='col-md-2 text-end'),
                Column(Reset('reset', 'Reset', css_class='btn btn-primary w-100'), css_class='col-md-2 text-end'),
            ),
        )
    
    class Meta:
        model = DigitizingOrder
        fields = '__all__'
        labels = {
            'name': 'Design Name',
            'height': 'Height (in inches)',
            'width': 'Width (in inches)',
            'colors': 'Number of Colors',
            'po_number': 'Purchase Order Number',
            'file_format': 'File Format',
            'fabric_type': 'Fabric Type',
            'logo_placement': 'Logo Placement',
            'instructions': 'Special Instructions',
            'is_urgent': 'Is this order urgent?',
        }
        widgets = {
            'instructions': forms.Textarea(attrs={'rows': 3})
        }

    def save(self, commit=True):
        order = super().save(commit=commit)
        file1 = self.cleaned_data.get('file1')
        file2 = self.cleaned_data.get('file2')

        if file1:
            DigitizingOrder_Files.objects.create(order=order, file=file1)
        if file2:
            DigitizingOrder_Files.objects.create(order=order, file=file2)

        return order


class PatchOrderForm(forms.ModelForm):

    file1 = forms.FileField(label='Upload Files (2 MB Max Size)', required=False)
    file2 = forms.FileField(label='', required=False)    

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(

            Row(
                Column('name', css_class='col-md-8'),
                Column('po_number', css_class='col-md-4'),
            ),
            Row(
                Column('height', css_class='col-md-6'),
                Column('width', css_class='col-md-6'),
                
            ),
            Row(
                Column('patch_type', css_class='col-md-6'),
                Column('backing_type', css_class='col-md-6'),
                
            ),
            Row(
                Column('border_type', css_class='col-md-6'),
                Column('embroidery_fill', css_class='col-md-6'),
                
            ),
            Row(
                Column('quantity', css_class='col-md-6'),
                Column('date', css_class='col-md-6'),
                
            ),
            Row(
                Column('color_details', css_class='col-md-12'),
                
            ),
            Row(
                Column('contact_name', css_class='col-md-6'),
                Column('contact_number', css_class='col-md-6'),
            ),
            Row(
                Column('shipping_address', css_class='col-md-6'),
                Column('instructions', css_class='col-md-6'),              
            ),
            Row(
                Column('file1', css_class='col-md-12'),
                Column('file2', css_class='col-md-12'),  
            ),  
            Row(
                Column(HTML(''), css_class='col-md-8'),
                Column(Submit('submit', 'Place Order', css_class='btn btn-primary w-100'), css_class='col-md-2 text-end'),
                Column(Reset('reset', 'Reset', css_class='btn btn-primary w-100'), css_class='col-md-2 text-end'),
            ),
        )
    
    def clean_file1(self):
        file1 = self.cleaned_data.get('file1')
        if file1:
            if file1.size > 2 * 1024 * 1024:  # 2 MB limit
                raise ValidationError("File 1 must be less than 2 MB.")
        return file1

    def clean_file2(self):
        file2 = self.cleaned_data.get('file2')
        if file2:
            if file2.size > 2 * 1024 * 1024:  # 2 MB limit
                raise ValidationError("File 2 must be less than 2 MB.")
        return file2

    class Meta:
        model = PatchOrder
        fields = '__all__'
        labels = {
            'name': 'Order Name',
            'height': 'Height (in inches)',
            'width': 'Width (in inches)',
            'colors': 'Number of Colors',
            'po_number': 'Purchase Order Number',
            'file_format': 'File Format',
            'fabric_type': 'Fabric Type',
            'logo_placement': 'Logo Placement',
            'instructions': 'Special Instructions',
        }
        widgets = {
            'instructions': forms.Textarea(attrs={'rows': 3}),
            'shipping_address': forms.Textarea(attrs={'rows': 3})
        }

    def save(self, commit=True):
        order = super().save(commit=commit)
        file1 = self.cleaned_data.get('file1')
        file2 = self.cleaned_data.get('file2')

        if file1:
            PatchOrder_Files.objects.create(order=order, file=file1)
        if file2:
            PatchOrder_Files.objects.create(order=order, file=file2)

        return order


class VectorOrderForm(forms.ModelForm):

    file1 = forms.FileField(label='Upload Files (2 MB Max Size)', required=False)
    file2 = forms.FileField(label='', required=False)    

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(

            Row(
                Column('name', css_class='col-md-8'),
                Column('po_number', css_class='col-md-4'),
            ),

            Row(
                Column('required_format', css_class='col-md-4'),
                Column('color_types', css_class='col-md-4'),
                Column('colors', css_class='col-md-4'),
                
            ),
            Row(
                
                Column('others', css_class='col-md-12'),
                
            ),

            Row(
                Column('instructions', css_class='col-md-6'),
                Column(Row(
                    Column('file1', css_class='col-md-12'),
                    Column('file2', css_class='col-md-12 mt-0'),  
                ), css_class='col-md-6'),                
            ),
            
            Row(
                Column(HTML(''), css_class='col-md-8'),
                Column(Submit('submit', 'Place Order', css_class='btn btn-primary w-100'), css_class='col-md-2 text-end'),
                Column(Reset('reset', 'Reset', css_class='btn btn-primary w-100'), css_class='col-md-2 text-end'),
            ),
        )
    
    def clean_file1(self):
        file1 = self.cleaned_data.get('file1')
        if file1:
            if file1.size > 2 * 1024 * 1024:  # 2 MB limit
                raise ValidationError("File 1 must be less than 2 MB.")
        return file1

    def clean_file2(self):
        file2 = self.cleaned_data.get('file2')
        if file2:
            if file2.size > 2 * 1024 * 1024:  # 2 MB limit
                raise ValidationError("File 2 must be less than 2 MB.")
        return file2

    class Meta:
        model = VectorOrder
        fields = '__all__'
        labels = {
            'name': 'Order Name',
            'colors': 'Number of Colors',
            'po_number': 'Purchase Order Number',
            'required_format': 'Required Format',
            'color_types': 'Color Type',
            'others': 'Others',
            'instructions': 'Additional Instructions',
        }
        widgets = {
            'instructions': forms.Textarea(attrs={'rows': 3}),
        }

    def save(self, commit=True):
        order = super().save(commit=commit)
        file1 = self.cleaned_data.get('file1')
        file2 = self.cleaned_data.get('file2')

        if file1:
            VectorOrder_Files.objects.create(order=order, file=file1)
        if file2:
            VectorOrder_Files.objects.create(order=order, file=file2)

        return order
    



###### QUOTES FORM ######

class DigitizingQuoteForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(

            Row(
                Column('name', css_class='col-md-12'),
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
                Column('instructions', css_class='col-md-12')               
            ),
            Row(
                Column('is_urgent', css_class='col-md-8'),
                Column(Submit('submit', 'Place Order', css_class='btn btn-primary w-100'), css_class='col-md-2 text-end'),
                Column(Reset('reset', 'Reset', css_class='btn btn-primary w-100'), css_class='col-md-2 text-end'),
            ),
        )
    
    class Meta:
        model = DigitizingQuote
        fields = '__all__'
        labels = {
            'name': 'Design Name',
            'height': 'Height (in inches)',
            'width': 'Width (in inches)',
            'colors': 'Number of Colors',
            'file_format': 'File Format',
            'fabric_type': 'Fabric Type',
            'logo_placement': 'Logo Placement',
            'instructions': 'Special Instructions',
            'is_urgent': 'Is this order urgent?',
        }
        widgets = {
            'instructions': forms.Textarea(attrs={'rows': 3})
        }

    def save(self, commit=True):
        order = super().save(commit=commit)
        return order
    


class PatchQuoteForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(

            Row(
                Column('name', css_class='col-md-6'),
                Column('height', css_class='col-md-3'),
                Column('width', css_class='col-md-3'),
            ),
            Row(
                Column('patch_type', css_class='col-md-6'),
                Column('backing_type', css_class='col-md-6'),
                
            ),
            Row(
                Column('border_type', css_class='col-md-6'),
                Column('embroidery_fill', css_class='col-md-6'),
                
            ),
            Row(
                Column('quantity', css_class='col-md-6'),
                Column('date', css_class='col-md-6'),
                
            ),
            Row(
                Column('color_details', css_class='col-md-12'),
                
            ),
            Row(
                Column('contact_name', css_class='col-md-6'),
                Column('contact_number', css_class='col-md-6'),
            ),
            Row(
                Column('shipping_address', css_class='col-md-6'),
                Column('instructions', css_class='col-md-6'),              
            ),
            Row(
                Column(HTML(''), css_class='col-md-8'),
                Column(Submit('submit', 'Place Order', css_class='btn btn-primary w-100'), css_class='col-md-2 text-end'),
                Column(Reset('reset', 'Reset', css_class='btn btn-primary w-100'), css_class='col-md-2 text-end'),
            ),
        )

    class Meta:
        model = PatchQuote
        fields = '__all__'
        labels = {
            'name': 'Order Name',
            'height': 'Height (in inches)',
            'width': 'Width (in inches)',
            'colors': 'Number of Colors',
            'file_format': 'File Format',
            'fabric_type': 'Fabric Type',
            'logo_placement': 'Logo Placement',
            'instructions': 'Special Instructions',
        }
        widgets = {
            'instructions': forms.Textarea(attrs={'rows': 3}),
            'shipping_address': forms.Textarea(attrs={'rows': 3})
        }

    def save(self, commit=True):
        order = super().save(commit=commit)
        return order
    


class VectorQuoteForm(forms.ModelForm):  

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(

            Row(
                Column('name', css_class='col-md-6'),
                Column('required_format', css_class='col-md-2'),
                Column('color_types', css_class='col-md-2'),
                Column('colors', css_class='col-md-2'),                
            ),
            Row(
                
                Column('others', css_class='col-md-12'),                
            ),

            Row(
                Column('instructions', css_class='col-md-12'),              
            ),
            
            Row(
                Column(HTML(''), css_class='col-md-8'),
                Column(Submit('submit', 'Place Order', css_class='btn btn-primary w-100'), css_class='col-md-2 text-end'),
                Column(Reset('reset', 'Reset', css_class='btn btn-primary w-100'), css_class='col-md-2 text-end'),
            ),
        )

    class Meta:
        model = VectorQuote
        fields = '__all__'
        labels = {
            'name': 'Order Name',
            'colors': 'Number of Colors',
            'required_format': 'Required Format',
            'color_types': 'Color Type',
            'others': 'Others',
            'instructions': 'Additional Instructions',
        }
        widgets = {
            'instructions': forms.Textarea(attrs={'rows': 3}),
        }

    def save(self, commit=True):
        order = super().save(commit=commit)
        return order