from django.urls import path

from .views import cart_home, cart_add, cart_remove

app_name = 'carts'

urlpatterns = [
    path('', cart_home, name='home'),
    path('add/', cart_add, name='add'),
    path('remove/', cart_remove, name='remove'),
]
