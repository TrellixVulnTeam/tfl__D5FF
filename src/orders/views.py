from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, DetailView
from django.shortcuts import redirect
from django.http import Http404, JsonResponse


from .models import Order


class AllOrdersView(LoginRequiredMixin, ListView):
    template_name = 'orders/home.html'

    def get_queryset(self):
        user = self.request.user
        return Order.objects.all(user)
        # return Order.objects.my_orders(self.request.user)

    def get_context_data(self, *args, **kwargs):
        context = super(AllOrdersView, self).get_context_data(*args, **kwargs)
        return context


class OrderDetailView(DetailView):
    template_name = "orders/detail.html"

    def get_object(self, *args, **kwargs):
        xid = self.kwargs.get('id')
        try:
            instance = Order.objects.get(id=xid)

            # instance.form = OrderForm()
            #
            # str = instance.cart.delivery
            # # date_object = datetime.strptime(str, '%d/%m/%y %H:%m')
            # # print(date_object)
            # print(str.year)
            # print(str.strftime("%d/%m/%Y %H:%M"))
            #
            # form = OrderForm(initial={
            #                     'manifestation': instance.cart.manifestation,
            #                     'address': instance.cart.address,
            #                     'beginning': instance.cart.beginning,
            #                     'ending': instance.cart.ending,
            #                     'delivery': str.strftime("%d/%m/%Y %H:%M"),
            #                     'pickup': instance.cart.pickup,
            #                     'personal_name': instance.cart.personal_name,
            #                     'email': instance.cart.email,
            #                     'phone': instance.cart.phone
            #                 })
            #
            # instance.form = form
            #
            #
            # str = instance.cart.delivery
            # #date_object = datetime.strptime(str, '%d/%m/%y %H:%m')
            # #print(date_object)
            # print(str.year)
            # print(str.strftime("%d/%m/%Y %H:%M"))
        except Order.DoesNotExist:
            raise Http404("Order doesn't exist!")
        except Order.MultipleObjectsReturned:
            qs = Order.objects.filter(id=xid)
            instance = qs.first()
        except:
            raise Http404("Uhhh")
        return instance


@csrf_exempt
def order_confirm(request, id):
    user = request.user
    if user.is_authenticated and (user.is_staff or user.is_admin):
        order_id = id
        if order_id is not None:
            try:
                order_obj = Order.objects.get(id=order_id)
                if order_obj.status != 'confirm' and order_obj.status != 'canceled':
                    order_obj.status = 'confirm'
                    order_obj.save()
            except Order.DoesNotExist:
                return redirect('orders:home')
    return JsonResponse({})
    # return redirect('orders:home')


@csrf_exempt
def order_edit(request, id):
    user = request.user
    data = {}
    if user.is_authenticated:
        try:
            order_obj = Order.objects.get(id=id)
            cart_obj = order_obj.cart
            request.session['cart_id'] = cart_obj.id
            request.session['cart_items'] = cart_obj.products.count()

            data = {
                'refresh': 'true'
            }
        except Order.DoesNotExist:
            return redirect('orders:home')
    return JsonResponse(data)
