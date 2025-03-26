from django import forms

from django.contrib.auth.forms import UserCreationForm
from crispy_bootstrap5.bootstrap5 import FloatingField
from crispy_forms.layout import Layout, Submit, Row, Column, Fieldset
from crispy_forms.helper import FormHelper
from .models import User

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