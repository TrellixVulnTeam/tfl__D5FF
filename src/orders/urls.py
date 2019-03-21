from django.urls import path

from .views import (
        AllOrdersView
)

app_name = 'orders'

urlpatterns = [
    path('', AllOrdersView.as_view(), name='home'),
    # path('add/', cart_add, name='add'),
    # path('checkout/', checkout_home, name='checkout'),
    # path('remove/', CartRemoveView.as_view(), name='remove'),
]
