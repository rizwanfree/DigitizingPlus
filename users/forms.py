from django import forms

from django.contrib.auth.forms import UserCreationForm
from crispy_bootstrap5.bootstrap5 import FloatingField
from crispy_forms.layout import Layout, Submit, Row, Column, Fieldset
from django.core.validators import MinValueValidator
from crispy_forms.helper import FormHelper
from .models import User
from crafting.models import BACKING_TYPE, BORDER_TYPE, FABRIC_CHOICES, LOGO_PLACEMENT, PATCH_TYPE, FORMAT_CHOICES


class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['user_id', 'email', 'password1', 'password2', 'first_name', 'last_name', 'phone_number', 'address', 'city', 'state', 'zip_code', 'country']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_action = 'users:register'
        self.helper.layout = Layout(
            Row(
                Column(FloatingField('first_name'), css_class='col-md-6'),
                Column(FloatingField('last_name'), css_class='col-md-6'),
                css_class='row'
            ),
            Row(
                Column(FloatingField('email'), css_class='col-md-4'),
                Column(FloatingField('phone_number'), css_class='col-md-2'),
                Column(FloatingField('address'), css_class='col-md-6'),
                css_class='row'
            ),
            Row(
                Column(FloatingField('city'), css_class='col-md-3'),
                Column(FloatingField('state'), css_class='col-md-3'),
                Column(FloatingField('zip_code'), css_class='col-md-3'),
                Column(FloatingField('country'), css_class='col-md-3'),
                css_class='row'
            ),
            Row(
                Column(FloatingField('user_id'), css_class='col-md-4'),
                Column(FloatingField('password1'), css_class='col-md-4'),
                Column(FloatingField('password2'), css_class='col-md-4'),
                css_class='row'
            ),
            Submit('submit', 'Register', css_class='btn btn-lg btn-primary w-100')
            
        )


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            'user_id', 'email', 'email2', 'email3',
            'first_name', 'last_name', 'phone_number',
            'address', 'city', 'state', 'zip_code', 'country', 'password'
        ]
        labels = {
            'email2': 'Email 2',
            'email3': 'Email 3'
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_tag = True
        self.helper.layout = Layout(

        Row(
            Column(FloatingField('user_id'), css_class='col-md-6'),
            Column(FloatingField('password'), css_class='col-md-6'),
            css_class='row'
        ),
        Row(
            Column(FloatingField('email'), css_class='col-md-4'),
            Column(FloatingField('email2'), css_class='col-md-4'),
            Column(FloatingField('email3'), css_class='col-md-4'),
            css_class='row'
        ),
            
            

        Row(
            Column(FloatingField('first_name'), css_class='col-md-4'),
            Column(FloatingField('last_name'), css_class='col-md-4'),
            Column(FloatingField('phone_number'), css_class='col-md-4'),
            css_class='row'
        ),
        
        
        FloatingField('address'),
        Row(
            Column(FloatingField('city'), css_class='col-md-3'),
            Column(FloatingField('state'), css_class='col-md-3'),
            Column(FloatingField('zip_code'), css_class='col-md-3'),
            Column(FloatingField('country'), css_class='col-md-3'),
            css_class='row'
        ),          
            
            
        Submit('submit', 'Update Profile', css_class='btn btn-primary w-100 mt-3')
        )
        
        # Make user_id readonly since it's the login field
        self.fields['user_id'].widget.attrs['readonly'] = True
        self.fields['user_id'].widget.attrs['class'] = 'form-control disable'


class GivenInfoForm(forms.Form):
    # Text fields
    design_name = forms.CharField(
        label="Design Name",
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        required=False,
    )
    
    po_number = forms.CharField(
        label="P.O. #",
        max_length=50,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'}),

    )
    
    # Numeric fields
    width = forms.DecimalField(
        label="Width (inches)",
        max_digits=5,
        decimal_places=2,
        validators=[MinValueValidator(0.01)],
        widget=forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
        required=False,    
    )
    
    height = forms.DecimalField(
        label="Height (inches)",
        max_digits=5,
        decimal_places=2,
        validators=[MinValueValidator(0.01)],
        required=False,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}))
    
    colors = forms.IntegerField(
        label="Colors",
        min_value=1,
        required=False,
        widget=forms.NumberInput(attrs={'class': 'form-control'}))
    
    
    required_format = forms.ChoiceField(
        label="Required Format",
        choices=FORMAT_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'}))
    
    
    placement = forms.ChoiceField(
        label="Placement",
        choices=LOGO_PLACEMENT,
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'}))
    
 
    
    fabric_type = forms.ChoiceField(
        label="Fabric Type",
        choices=FABRIC_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'}))
    
    # Price fields
    price_option_a = forms.DecimalField(
        label="Price Option A ($)",
        max_digits=8,
        decimal_places=2,
        required=False,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}))
    
    price_option_b = forms.DecimalField(
        label="Price Option B ($)",
        max_digits=8,
        decimal_places=2,
        required=False,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}))
    
    total_price = forms.DecimalField(
        label="Total Price ($)",
        max_digits=8,
        decimal_places=2,
        required=False,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'step': '0.01',
            'readonly': 'readonly'  # Often calculated automatically
    }))



class OptionsForm(forms.Form):
    width_a = forms.DecimalField(
        label="Width (inches)",
        max_digits=5,
        decimal_places=2,
        validators=[MinValueValidator(0.01)],
        widget=forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
        required=False,    
    )
    
    height_a = forms.DecimalField(
        label="Height (inches)",
        max_digits=5,
        decimal_places=2,
        validators=[MinValueValidator(0.01)],
        required=False,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}))
    
    stitches_a = forms.IntegerField(
        label="Stitches",
        min_value=1,
        required=False,
        widget=forms.NumberInput(attrs={'class': 'form-control'}))
    
    price_a = forms.DecimalField(
        label="Price",
        max_digits=5,
        decimal_places=2,
        validators=[MinValueValidator(0.01)],
        required=False,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}))
    
    width_b = forms.DecimalField(
        label="Width (inches)",
        max_digits=5,
        decimal_places=2,
        validators=[MinValueValidator(0.01)],
        widget=forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
        required=False,    
    )
    
    height_b = forms.DecimalField(
        label="Height (inches)",
        max_digits=5,
        decimal_places=2,
        validators=[MinValueValidator(0.01)],
        required=False,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}))
    
    stitches_b = forms.IntegerField(
        label="Stitches",
        min_value=1,
        required=False,
        widget=forms.NumberInput(attrs={'class': 'form-control'}))
    
    price_b = forms.DecimalField(
        label="Price",
        max_digits=5,
        decimal_places=2,
        validators=[MinValueValidator(0.01)],
        required=False,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}))
    
        # Summary Fields
    total_price = forms.DecimalField(
        label="Total Price",
        max_digits=8, decimal_places=2,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'readonly': True,
            'step': '0.01'
        })
    )
    
    comments = forms.CharField(
        label="Comments",
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3
        }),
        required=False
    )
