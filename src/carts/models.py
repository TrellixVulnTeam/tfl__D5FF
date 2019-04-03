from django.conf import settings
from django.db import models
from django.db.models.signals import pre_save, post_save, m2m_changed


from products.models import CartProduct

User = settings.AUTH_USER_MODEL


class CartManager(models.Manager):
    def new_or_get(self, request):
        cart_id = request.session.get('cart_id', None)
        qs = self.get_queryset().filter(id=cart_id)
        if qs.count() == 1:
            new_obj = False
            cart_obj = qs.first()
            if request.user.is_authenticated and cart_obj.user is None:
                cart_obj.user = request.user
                cart_obj.save()
        else:
            cart_obj = Cart.objects.new(user=request.user)
            new_obj = True
            request.session['cart_id'] = cart_obj.id
        return cart_obj, new_obj

    def new(self, user=None):
        user_obj = None
        if user is not None:
            if user.is_authenticated:
                user_obj = user
        return self.model.objects.create(user=user_obj)


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    manifestation = models.CharField(max_length=255, blank=False, null=True)
    beginning = models.DateTimeField(null=True, blank=False)
    ending = models.DateTimeField(null=True, blank=False)
    delivery = models.DateTimeField(null=True, blank=False)
    pickup = models.DateTimeField(null=True, blank=False)
    email = models.EmailField(max_length=255, null=True)
    personal_name = models.CharField(max_length=255, blank=False, null=True)
    address = models.CharField(max_length=255, blank=False, null=True)
    phone = models.CharField(max_length=255, blank=False, null=True)
    products = models.ManyToManyField(CartProduct, blank=True)
    total_price = models.DecimalField(default=0.00, max_digits=100, decimal_places=2)
    total_weight = models.DecimalField(default=0.00, max_digits=100, decimal_places=2)
    updated = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    objects = CartManager()

    def __str__(self):
        return str(self.id)


def pre_save_cart_receiver(sender, instance, action, *args, **kwargs):
    if action == 'post_add' or action == 'post_remove' or action == 'post_clear':
        products = instance.products.all()
        total_price = 0
        total_weight = 0
        for p in products:
            total_price += p.product.price * p.quantity
            total_weight += p.product.weight * p.quantity

        instance.total_price = total_price
        instance.total_weight = total_weight
        instance.save()


def pre_save_cart_product_receiver(sender, instance, action, *args, **kwargs):
    if action == 'post_add' or action == 'post_remove' or action == 'post_clear':
        products = instance.products.all()
        total_price = 0
        total_weight = 0
        for p in products:
            total_price += p.product.price * p.quantity
            total_weight += p.product.weight * p.quantity

        instance.total_price = total_price
        instance.total_weight = total_weight
        instance.save()


m2m_changed.connect(pre_save_cart_receiver, sender=Cart.products.through)


def update_cart_total(sender, instance, **kwargs):
    post_save.disconnect(update_cart_total, sender=sender)

    products = instance.products.all()
    total_price = 0
    total_weight = 0
    for p in products:
        total_price += p.product.price * p.quantity
        total_weight += p.product.weight * p.quantity

    instance.total_price = total_price
    instance.total_weight = total_weight
    instance.save()

    post_save.connect(update_cart_total, sender=sender)


post_save.connect(update_cart_total, sender=Cart)
