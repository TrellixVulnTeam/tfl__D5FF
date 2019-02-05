from django.db import models
from django.db.models import Q

from carts.models import Cart
from products.models import Product


class ProductQuantityQuerySet(models.query.QuerySet):
    def get_product_quantity(self, cart_obj, product_obj):
        lookups = (Q(cart=cart_obj) &
                   Q(product=product_obj))
        return self.filter(lookups).first()


class ProductQuantityManager(models.Manager):
    def get_queryset(self):
        return ProductQuantityQuerySet(self.model, using=self._db)

    def new(self, cart_obj, product_obj):
        product_quantity = self.get_queryset().get_product_quantity(cart_obj, product_obj)
        if product_quantity is None:
            self.model.objects.create(cart=cart_obj, product=product_obj)
        else:
            product_quantity.quantity = 1
            product_quantity.save()


class ProductQuantity(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    updated = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    objects = ProductQuantityManager()

    class Meta:
        unique_together = (('cart', 'product'),)
