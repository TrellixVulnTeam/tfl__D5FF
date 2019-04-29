from django.urls import path

from .views import (
    ProductListView,
    ProductDetailView,
    ProductDetailUpdateView,
    cart_add
)


app_name = 'products'

urlpatterns = [
    path('', ProductListView.as_view(), name='list'),
    path('<int:company>/', ProductListView.as_view(), name='company_products'),
    path('<slug:slug>/', ProductDetailView.as_view(), name='detail'),
    path('<slug:slug>/edit/', ProductDetailUpdateView.as_view(), name='edit'),
    path('cart/add/', cart_add, name='add'),

    # path('<slug:slug>/cart/add/', cart_add, name='add_to_cart'),
    # path('<int:company>/cart/add/', cart_add, name='add_to_cart'),
    # path('<int:company>/<slug:slug>/cart/add/', cart_add, name='add_to_cart'),

]
