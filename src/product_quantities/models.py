from django.db import models

from carts.models import Cart
from products.models import Product


class ProductQuantityManager(models.Manager):
    def new(self, cart_obj, product_obj):
        self.model.objects.create(cart=cart_obj, product=product_obj)


class ProductQuantity(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)
    updated = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    objects = ProductQuantityManager()

    class Meta:
        unique_together = (('cart', 'product'),)
