from django.urls import path
from .views import create_payment_transaction,payment_status,home


urlpatterns = [
   
    path('create_payment_transaction/', create_payment_transaction, name='create_payment_transaction'),
    path('payment-status/', payment_status, name='payment_status'),
    path('',home,name='home')
 
]

