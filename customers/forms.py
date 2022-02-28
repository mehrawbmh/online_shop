import django.contrib.auth.password_validation
from django.core.exceptions import ValidationError
from django.forms import ModelForm, Widget, BoundField
from django import forms
from django.utils.datetime_safe import datetime

from core.validators import is_all_numeric
from .models import Customer
from core.models import User


class CustomerForm(ModelForm):
    class Meta:
        model = User
        fields = ['phone', 'first_name', 'last_name', 'email']

    birthday = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'type': 'date'}),
        initial=datetime(2000, 1, 1, ).date(),
    )
    national_code = forms.CharField(
        max_length=10,
        min_length=10,
        validators=[is_all_numeric]
    )
    password = forms.CharField(
        min_length=8,
        validators=[django.contrib.auth.password_validation.validate_password],
        widget=forms.PasswordInput
    )
    password_confirm = forms.CharField(
        min_length=8,
        widget=forms.PasswordInput
    )

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data['password'] != cleaned_data['password_confirm']:
            self.add_error(
                'password_confirm',
                ValidationError("Password confirmation doesn't match with password")
            )
