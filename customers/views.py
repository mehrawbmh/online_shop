from django.contrib.auth.views import LoginView
from django.shortcuts import render


class CustomerLoginView(LoginView):
    template_name = 'registration/login.html'

