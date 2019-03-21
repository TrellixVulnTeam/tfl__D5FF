from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView

from .models import Order


class AllOrdersView(LoginRequiredMixin, ListView):
    template_name = 'orders/home.html'

    def get_queryset(self):
        return Order.objects.all()

    def get_context_data(self, *args, **kwargs):
        context = super(AllOrdersView, self).get_context_data(*args, **kwargs)
        return context
