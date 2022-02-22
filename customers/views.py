from django.contrib.auth.views import LoginView
from django.shortcuts import render
from django.views.generic import CreateView
from customers.models import Customer


class CustomerLoginView(LoginView):
    template_name = 'registration/login.html'


class CustomerSignUpView(CreateView):
    model = Customer
    template_name = 'registration/signup.html'
    fields = '__all__'