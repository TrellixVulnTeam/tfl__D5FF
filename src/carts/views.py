from django.urls import reverse
from django.shortcuts import render, redirect
from django.views.generic import UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from products.models import Product, CartProduct
from .models import Cart
from .forms import CartForm
from orders.models import Order
from companies.models import Company
from tfl.mixins import NextUrlMixin
from tfl import utils


class CartView(LoginRequiredMixin, NextUrlMixin, UpdateView):
    form_class = CartForm
    template_name = 'carts/home.html'
    success_url = '/cart'

    def get_object(self, queryset=None):
        cart_obj, new_obj = Cart.objects.new_or_get(self.request)
        return cart_obj


# @csrf_exempt
# class CartRemoveView(LoginRequiredMixin, NextUrlMixin, DeleteView):
#     form_class = CartForm
#     template_name = 'carts/home.html'
#     success_url = '/cart'
#
#     # def get_object(self, queryset=None):
#     #     cart_obj, new_obj = Cart.objects.new_or_get(self.request)
#     #     return cart_obj
#
#     def get_object(self, queryset=None):
#         request = self.request
#         product_id = request.POST.get('product_id')
#         if product_id is not None:
#             try:
#                 product_obj = Product.objects.get(id=product_id)
#             except Product.DoesNotExist:
#                 return redirect('cart:home')
#             cart_obj, new_obj = Cart.objects.new_or_get(request)
#             for p in cart_obj.products.all():
#                 if p.product == product_obj:
#                     cart_obj.products.remove(p)
#                     request.session['cart_items'] = cart_obj.products.count()
#                     # return p  # automatski brise iz baze objekat p
#         return None
#
#     def get_success_url(self):
#         return reverse('cart:home')

# def cart_home(request):
#     form = CartForm()
#     cart_obj, new_obj = Cart.objects.new_or_get(request)
#     context = {
#         'form': form,
#         'cart': cart_obj,
#     }
#     return render(request, 'carts/home.html', context)

# def cart_add(request):
#     product_id = request.POST.get('product_id')
#     if product_id is not None:
#         try:
#             product_obj = Product.objects.get(id=product_id)
#         except Product.DoesNotExist:
#             return redirect('cart:home')
#         cart_obj, new_obj = Cart.objects.new_or_get(request)
#         find = False
#         for p in cart_obj.products.all():
#             if p.product == product_obj:
#                 find = True
#         if not find:
#             cart_product = CartProduct.objects.new(product=product_obj)
#             cart_obj.products.add(cart_product)
#         request.session['cart_items'] = cart_obj.products.count()
#     return redirect('cart:home')


# def cart_remove(request):
#     product_id = request.POST.get('product_id')
#     if product_id is not None:
#         try:
#             product_obj = Product.objects.get(id=product_id)
#         except Product.DoesNotExist:
#             return redirect('cart:home')
#         cart_obj, new_obj = Cart.objects.new_or_get(request)
#         for p in cart_obj.products.all():
#             if p.product == product_obj:
#                 cart_obj.products.remove(p)
#         request.session['cart_items'] = cart_obj.products.count()
#     return redirect('cart:home')


def checkout_home(request):
    cart_obj, cart_created = Cart.objects.new_or_get(request)
    order_obj = None
    if cart_created or cart_obj.products.count() == 0:
        msg = 'Cart is empty!'
        messages.warning(request, msg)

        return redirect('cart:home')
    else:
        # if request.method == 'POST':
        #     form = CartForm(request.POST)
        #     if form.is_valid():
        #         cart_obj.manifestation = form.cleaned_data.get('manifestation')
        #         cart_obj.address = form.cleaned_data.get('address')
        #         cart_obj.beginning = form.cleaned_data.get('beginning')
        #         cart_obj.ending = form.cleaned_data.get('ending')
        #         cart_obj.delivery = form.cleaned_data.get('delivery')
        #         cart_obj.pickup = form.cleaned_data.get('pickup')
        #         cart_obj.personal_name = form.cleaned_data.get('personal_name')
        #         cart_obj.email = form.cleaned_data.get('email')
        #         cart_obj.phone = form.cleaned_data.get('phone')
        #         cart_obj.save()
        # else:
        #     form = CartForm()

        # old_order_id = request.session.get('order_id')
        # if old_order_id is not None:
        #     old_order_obj = Order.objects.get(id=old_order_id)
        #     old_order_obj.deactivate()
        order_obj, new_order_obj = Order.objects.get_or_create(cart=cart_obj)
        request.session['cart_id'] = None
        request.session['cart_items'] = 0
        msg = 'You have successfully made an order!'
        messages.success(request, msg)
    return redirect('orders:home')


@csrf_exempt
def cart_field_change(request):
    field_name = request.POST.get('field_name')
    field_value = request.POST.get('field_value')
    date_field = request.POST.get('date_field')
    error = None
    error_message = ""

    data = {
        "error": error,
        "error_message": error_message
    }

    if date_field == '1':
        field_value, error = utils.get_date_obj(field_value)
        error, error_message = Cart.objects.check_date_field(request=request, field_name=field_name, field_value=field_value)

        if error is True:
            data["error"] = 'true'
            data["error_message"] = error_message

    if (error is False or error is None) and field_value is not None:
        cart_obj, new_obj = Cart.objects.new_or_get(request)
        setattr(cart_obj, field_name, field_value)
        cart_obj.save()

    return JsonResponse(data)


@csrf_exempt
def clean_date(request):
    field_name = request.POST.get('field_name')
    field_value = None

    cart_obj, new_obj = Cart.objects.new_or_get(request)
    setattr(cart_obj, field_name, field_value)
    cart_obj.save()

    return JsonResponse({})


@csrf_exempt
def set_company(request):
    company_id = request.POST.get('company_id')
    company_obj = Company.objects.get_by_id(company_id)
    cart_obj, new_obj = Cart.objects.new_or_get(request)
    setattr(cart_obj, 'company', company_obj)
    cart_obj.save()

    return JsonResponse({})


@csrf_exempt
def validate_quantity(request):
    product_id = request.POST.get('product_id', None)
    product_quantity = request.POST.get('product_quantity', None)
    data = None

    try:
        product_obj = Product.objects.get(id=product_id)
        cart_obj, new_obj = Cart.objects.new_or_get(request)
        # for p in cart_obj.products.all():
        #     if p.product == product_obj:
        #         p.quantity = product_quantity
        #         p.save()
        #         cart_obj.save()
        #
        #         data = {
        #             'total_weight': cart_obj.total_weight,
        #             'total_price': cart_obj.total_price
        #         }
        data = cart_obj.validate_quantity(product_obj, product_quantity)
    except Product.DoesNotExist:
        return redirect('cart:home')

    return JsonResponse(data)


@csrf_exempt
def cart_remove(request):
    product_id = request.POST.get('product_id')
    data = None
    if product_id is not None:
        try:
            product_obj = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return redirect('cart:home')
        cart_obj, new_obj = Cart.objects.new_or_get(request)
        for p in cart_obj.products.all():
            if p.product == product_obj:
                cart_obj.products.remove(p)
        request.session['cart_items'] = cart_obj.products.count()

        data = {
            'refresh': 'true'
        }

    return JsonResponse(data)
