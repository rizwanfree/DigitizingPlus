from django import forms

from django.contrib.auth.forms import UserCreationForm
from crispy_bootstrap5.bootstrap5 import FloatingField
from crispy_forms.layout import Layout, Submit, Row, Column
from crispy_forms.helper import FormHelper

from .models import User


class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = User

        fields = ['email', 'password1', 'password2', 'first_name', 'last_name', 'phone_number', 'address', 'city', 'state', 'zip_code', 'country']

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
                Column(FloatingField('password1'), css_class='col-md-6'),
                Column(FloatingField('password2'), css_class='col-md-6'),
                css_class='row'
            ),
            Submit('submit', 'Register', css_class='btn btn-lg btn-primary w-100')
        )