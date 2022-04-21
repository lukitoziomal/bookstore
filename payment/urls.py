from django.urls import path, include
from . import views

app_name = 'payment'
urlpatterns = [
    path('paypal', views.PaypalFormView.as_view(), name='paypal-payment'),
    path('paypal-cancel', views.payment_cancelled, name='paypal-cancel'),
    path('paypal-return', views.payment_done, name='paypal-return')
]