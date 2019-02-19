from django.urls import reverse
from django.shortcuts import render, redirect
from django.views.generic import UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin

from products.models import Product, CartProduct
from .models import Cart
from .forms import CartForm
from orders.models import Order
from tfl.mixins import NextUrlMixin


class CartView(LoginRequiredMixin, NextUrlMixin, UpdateView):
    form_class = CartForm
    template_name = 'carts/home.html'
    success_url = '/cart'

    def get_object(self, queryset=None):
        cart_obj, new_obj = Cart.objects.new_or_get(self.request)
        return cart_obj


class CartRemoveView(LoginRequiredMixin, NextUrlMixin, DeleteView):
    form_class = CartForm
    template_name = 'carts/home.html'
    success_url = '/cart'

    # def get_object(self, queryset=None):
    #     cart_obj, new_obj = Cart.objects.new_or_get(self.request)
    #     return cart_obj

    def get_object(self, queryset=None):
        request = self.request
        product_id = request.POST.get('product_id')
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
                    return p  # automatski brise iz baze objekat p
        return None

    def get_success_url(self):
        return reverse('cart:home')

# def cart_home(request):
#     form = CartForm()
#     cart_obj, new_obj = Cart.objects.new_or_get(request)
#     context = {
#         'form': form,
#         'cart': cart_obj,
#     }
#     return render(request, 'carts/home.html', context)


def cart_add(request):
    product_id = request.POST.get('product_id')
    if product_id is not None:
        try:
            product_obj = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return redirect('cart:home')
        cart_obj, new_obj = Cart.objects.new_or_get(request)
        find = False
        for p in cart_obj.products.all():
            if p.product == product_obj:
                find = True
        if not find:
            cart_product = CartProduct.objects.new(product=product_obj)
            cart_obj.products.add(cart_product)
        request.session['cart_items'] = cart_obj.products.count()
    return redirect('cart:home')


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
        return redirect('cart:home')
    else:
        order_obj, new_order_obj = Order.objects.get_or_create(cart=cart_obj)
    return render(request, 'carts/checkout.html', {'object': order_obj})
