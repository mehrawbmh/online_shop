from django.urls import path
from .views import CustomerLoginView
urlpatterns = [
    path('login/', CustomerLoginView.as_view(), name='login'),
    path('login/', CustomerLoginView.as_view(), name='login_view')
]