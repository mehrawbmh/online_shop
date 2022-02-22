from django.forms import ModelForm
from .models import Customer


class CustomerForm(ModelForm):
    model = Customer
    fields = '__all__'
