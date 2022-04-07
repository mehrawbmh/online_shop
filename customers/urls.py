from django.urls import path
from django.views.generic import TemplateView

from .apis import CustomerViewSet, UserDetailAPIView
from .views import CustomerLoginView, CustomerSignUpView, CustomerProfileView
from django.contrib.auth.views import LogoutView
urlpatterns = [
    path('logout/', LogoutView.as_view(), name='logout_view'),
    path('contact-us/', TemplateView.as_view(template_name='customers/contact_us.html'), name='contact-us'),
    path('login/', CustomerLoginView.as_view(), name='login_view'),
    path('register/', CustomerSignUpView.as_view(), name='register_view'),
    path('signup/', CustomerSignUpView.as_view(), name='register'),
    path('profile/<int:pk>', CustomerProfileView.as_view(), name='customer_profile'),
    path('user-detail/<int:pk>', UserDetailAPIView.as_view(), name='user-detail'),
    path('customers_api/', CustomerViewSet.as_view(
        {
            'get': 'list',
            'post': 'create',
            'delete': 'destroy'
        }
    ))
]
