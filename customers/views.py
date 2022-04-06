from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import AnonymousUser
from django.contrib.auth.views import LoginView
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import FormView, DetailView
from django.contrib.auth import login as auth_login
from core.models import User
from customers.forms import CustomerForm
from customers.models import Customer
from django.forms import Form

from orders.models import CartItem, Cart


class CustomerLoginView(LoginView):
    template_name = 'registration/login.html'

    def form_valid(self, form):
        auth_login(self.request, form.get_user())
        try:
            products_id_list = [(int(x[4:]), y) for x, y in self.request.COOKIES.items() if x.startswith('prod')]
        except ValueError:
            return HttpResponseRedirect(self.get_success_url())

        last_cart: Cart = self.request.user.customer.cart_set.last()
        if last_cart and last_cart.status == 'unfinished':
            ids = list(map(lambda my_tuple: int(my_tuple[0]), products_id_list))
            for cartitem in last_cart.items.all():
                if cartitem.product.id in ids:
                    cartitem.count += abs(int(self.request.COOKIES.get(f'prod{cartitem.product.id}')))
                    cartitem.save()
            cart_item_objects = [CartItem(product_id=int(x), count=y, cart=last_cart) for x, y in products_id_list]
            CartItem.objects.bulk_create(cart_item_objects)
        else:
            new_cart = Cart.objects.create(customer=self.request.user.customer)
            cart_item_objects = [CartItem(product_id=int(x), count=y, cart=new_cart) for x, y in products_id_list]
            CartItem.objects.bulk_create(cart_item_objects)
            print('iin')
        print(cart_item_objects, 'Anjam shod')

        return HttpResponseRedirect(self.get_success_url())


class CustomerSignUpView(FormView):
    template_name = 'registration/signup.html'
    form_class = CustomerForm

    # pro_id = 0
    # success_url = reverse_lazy('customer_profile', args={'pk':pro_id})

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
        related_user = User.objects.create_user(
            form['phone'].value(),
            form['email'].value(),
            form['password'].value(),
            phone=form['phone'].value(),
            first_name=form['first_name'].value(),
            last_name=form['last_name'].value()
        )
        customer = Customer.objects.create(
            birthday=form['birthday'].value(),
            national_code=form['national_code'].value(),
            user=related_user
        )
        return redirect(reverse_lazy('customer_profile', kwargs={'pk': customer.id}))
        # self.__class__.pro_id = customer.id
        # return super().form_valid(form)

    def form_invalid(self, form):
        return render(self.request, template_name=self.template_name, context={'form': form})


class CustomerProfileView(DetailView):
    context_object_name = 'customer'
    template_name = 'customers/profile.html'
    queryset = Customer.objects.all()
    model = Customer

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        self.object: Customer
        context['last_cart'] = self.object.cart_set.last()
        return context

    def get(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated or kwargs['pk'] != self.request.user.customer.id:
            return HttpResponse(status=403)
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)
