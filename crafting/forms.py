from django import forms
from django.core.exceptions import ValidationError
from .models import DigitizingOrder, PatchOrder, VectorOrder, DigitizingOrder_Files, PatchOrder_Files, VectorOrder_Files, DigitizingQuote, PatchQuote, VectorQuote
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Submit, Reset, HTML

class BaseOrderForm:
    """Base form class with common functionality for all order forms"""
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)  # Get user from kwargs
        super().__init__(*args, **kwargs)
        # Remove user field from form as we'll set it automatically
        if 'user' in self.fields:
            del self.fields['user']

    def save(self, commit=True):
        # Set the user before saving
        instance = super().save(commit=False)
        if self.user:
            instance.user = self.user
        if commit:
            instance.save()
        return instance

class DigitizingOrderForm(BaseOrderForm, forms.ModelForm):
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
        exclude = ['user', 'status', 'created_at']  # Exclude auto fields
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

class PatchOrderForm(BaseOrderForm, forms.ModelForm):
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
        exclude = ['user', 'status', 'created_at']
        labels = {
            'name': 'Order Name',
            'height': 'Height (in inches)',
            'width': 'Width (in inches)',
            'po_number': 'Purchase Order Number',
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

class VectorOrderForm(BaseOrderForm, forms.ModelForm):
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
        exclude = ['user', 'status', 'created_at']
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

###### QUOTE FORMS ######

class DigitizingQuoteForm(BaseOrderForm, forms.ModelForm):
    class Meta:
        model = DigitizingQuote
        exclude = ['user', 'created_at']
        widgets = {
            'instructions': forms.Textarea(attrs={'rows': 3})
        }

class PatchQuoteForm(BaseOrderForm, forms.ModelForm):
    class Meta:
        model = PatchQuote
        exclude = ['user', 'created_at']
        widgets = {
            'instructions': forms.Textarea(attrs={'rows': 3}),
            'shipping_address': forms.Textarea(attrs={'rows': 3})
        }

class VectorQuoteForm(BaseOrderForm, forms.ModelForm):
    class Meta:
        model = VectorQuote
        exclude = ['user', 'created_at']
        widgets = {
            'instructions': forms.Textarea(attrs={'rows': 3}),
        }