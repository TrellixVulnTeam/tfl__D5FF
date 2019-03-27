from django.urls import path

from .views import (
        AllOrdersView,
        OrderDetailView,
        order_confirm
)

app_name = 'orders'

urlpatterns = [
    path('', AllOrdersView.as_view(), name='home'),
    path('<slug:id>/', OrderDetailView.as_view(), name='detail'),
    path('confirm/', order_confirm, name='confirm'),
]
