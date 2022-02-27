from django.contrib.auth.views import LoginView
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import FormView, DetailView
from customers.forms import CustomerForm
from customers.models import Customer
from django.forms import Form


class CustomerLoginView(LoginView):
    template_name = 'registration/login.html'


class CustomerSignUpView(FormView):
    template_name = 'registration/signup.html'
    form_class = CustomerForm
    success_url = reverse_lazy('customer_profile')

    # def get(self, req, *args, **kwargs):
    #     return super().get(req, *args, **kwargs)
    #
    # def post(self, request, *args, **kwargs):
    #     form: Form = self.get_form()
    #     if form.is_valid():
    #         return super().post(request, *args, **kwargs)
    #     else:
    #         return render(request, template_name=self.get_template_names(), context={'forms':self.get_context_data()})
    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['form'] = self.get_form()
    #     return context

    def form_valid(self, form):
        pass

    def form_invalid(self, form):
        return render(self.request, template_name=self.template_name, context={'form': form})


class CustomerProfileView(DetailView):
    context_object_name = 'customer'
    template_name = 'customers/profile.html'
    queryset = Customer.objects.all()
    # model = Customer
