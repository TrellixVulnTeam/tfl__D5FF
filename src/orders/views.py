from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView
from django.shortcuts import redirect
from django.http import Http404

from .models import Order


class AllOrdersView(LoginRequiredMixin, ListView):
    template_name = 'orders/home.html'

    def get_queryset(self):
        return Order.objects.all()

    def get_context_data(self, *args, **kwargs):
        context = super(AllOrdersView, self).get_context_data(*args, **kwargs)
        return context


class OrderDetailView(DetailView):
    #queryset = Order.objects.all()
    template_name = "orders/detail.html"


    def get_object(self, *args, **kwargs):
        # request = self.request
        id = self.kwargs.get('id')
        try:
            instance = Order.objects.get(id=id)
        except Order.DoesNotExist:
            raise Http404("Order doesn't exist!")
        except Order.MultipleObjectsReturned:
            qs = Order.objects.filter(id=id)
            instance = qs.first()
        except:
            raise Http404("Uhhh")
        return instance


def order_confirm(request):
    order_id = request.POST.get('order_id')
    if order_id is not None:
        try:
            order_obj = Order.objects.get(id=order_id)
        except Order.DoesNotExist:
            return redirect('orders:home')

        if order_obj.status != 'confirm' and order_obj.status != 'canceled':
            order_obj.status = 'confirm'
            order_obj.save()

    return redirect('orders:home')
