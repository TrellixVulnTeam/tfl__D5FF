from django.urls import path

from .views import (
        CartView,
        # CartRemoveView,
        # cart_add,
        cart_field_change,
        cart_remove,
        checkout_home,
        validate_quantity
)

app_name = 'cart'

urlpatterns = [
    # path('', cart_home, name='home'),
    path('', CartView.as_view(), name='home'),
    # path('add/', cart_add, name='add'),
    path('checkout/', checkout_home, name='checkout'),
    # path('remove/', CartRemoveView.as_view(), name='remove'),
    path('cart_field_change/', cart_field_change, name='field_change'),
    path('remove/', cart_remove, name='remove'),
    path('validate_quantity/', validate_quantity, name='validate'),
]
