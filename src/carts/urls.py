from django.urls import path

from .views import (
        CartView,
        CartRemoveView,
        cart_add,
        checkout_home
)

app_name = 'cart'

urlpatterns = [
    # path('', cart_home, name='home'),
    path('', CartView.as_view(), name='home'),
    path('add/', cart_add, name='add'),
    path('checkout/', checkout_home, name='checkout'),
    path('remove/', CartRemoveView.as_view(), name='remove'),
    # path('remove/', cart_remove, name='remove'),
]
