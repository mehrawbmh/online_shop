from django.forms import ModelForm, Widget, BoundField
from django import forms

from core.validators import is_all_numeric
from .models import Customer
from core.models import User


class CustomerForm(ModelForm):
    class Meta:
        model = User
        fields = ['phone', 'first_name', 'last_name', 'password']

    birthday = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'type': 'date'})
    )
    national_code = forms.CharField(
        max_length=10,
        min_length=10,
        validators=[is_all_numeric]
    )
