from django.urls import path
from .apis import CustomerViewSet, UserDetailAPIView
from .views import CustomerLoginView, CustomerSignUpView, CustomerProfileView

urlpatterns = [
    path('login/', CustomerLoginView.as_view(), name='login'),
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
        }))
]
