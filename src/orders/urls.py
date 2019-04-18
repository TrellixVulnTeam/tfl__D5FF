from django.urls import path

from .views import (
        AllOrdersView,
        OrderDetailView,
        order_confirm,
        order_edit
)

app_name = 'orders'

urlpatterns = [
    path('', AllOrdersView.as_view(), name='home'),
    path('<slug:id>/', OrderDetailView.as_view(), name='detail'),
    path('<slug:id>/confirm/', order_confirm, name='confirm'),
    path('<slug:id>/edit_order/', order_edit, name='edit'),
    # path('confirm/', order_confirm, name='confirm'),
]
