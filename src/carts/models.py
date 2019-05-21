from django.conf import settings
from django.db import models
from django.db.models.signals import pre_save, post_save, m2m_changed
from django.apps import apps


from products.models import CartProduct
from companies.models import Company

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
                company = user.company
        return self.model.objects.create(user=user_obj, company=company)

    def check_date_field(self, request, field_name, field_value):
        cart_obj, new_obj = self.new_or_get(request=request)
        error = None
        error_message = ""

        if field_value is not None:
            if field_name == 'beginning':
                if cart_obj.ending is not None:
                    if cart_obj.ending <= field_value:
                        error = True
                        error_message = "Beginning date is not valid!"
                if cart_obj.delivery is not None:
                    if cart_obj.delivery >= field_value:
                        error = True
                        error_message = "Beginning date is not valid!"
                if cart_obj.pickup is not None:
                    if cart_obj.pickup <= field_value:
                        error = True
                        error_message = "Beginning date is not valid!"
            elif field_name == 'ending':
                if cart_obj.beginning is not None:
                    if cart_obj.beginning >= field_value:
                        error = True
                        error_message = "Ending date is not valid!"
                if cart_obj.delivery is not None:
                    if cart_obj.delivery >= field_value:
                        error = True
                        error_message = "Ending date is not valid!"
                if cart_obj.pickup is not None:
                    if cart_obj.pickup <= field_value:
                        error = True
                        error_message = "Ending date is not valid!"
            elif field_name == 'delivery':
                if cart_obj.beginning is not None:
                    if cart_obj.beginning <= field_value:
                        error = True
                        error_message = "Delivery date is not valid!"
                if cart_obj.ending is not None:
                    if cart_obj.ending <= field_value:
                        error = True
                        error_message = "Delivery date is not valid!"
                if cart_obj.pickup is not None:
                    if cart_obj.pickup <= field_value:
                        error = True
                        error_message = "Delivery date is not valid!"
            elif field_name == 'pickup':
                if cart_obj.beginning is not None:
                    if cart_obj.beginning >= field_value:
                        error = True
                        error_message = "Pickup date is not valid!"
                if cart_obj.ending is not None:
                    if cart_obj.ending >= field_value:
                        error = True
                        error_message = "Pickup date is not valid!"
                if cart_obj.delivery is not None:
                    if cart_obj.delivery >= field_value:
                        error = True
                        error_message = "Pickup date is not valid!"

        return error, error_message


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
    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True, blank=True, default=4)

    objects = CartManager()

    def __str__(self):
        return str(self.id)

    # def save(self, *args, **kwargs):
    #     self.beginning = self.beginning.replace(tzinfo=None)
    #     self.ending = self.ending.replace(tzinfo=None)
    #     self.delivery = self.delivery.replace(tzinfo=None)
    #     self.pickup = self.pickup.replace(tzinfo=None)
    #     super(Cart, self).save(*args, **kwargs)

    def validate_quantity(self, product_obj, product_quantity):
        data = {}
        # self.objects.num_unavailable_products(product_obj)
        cart_products_obj = CartProduct.objects.get_by_product(product_obj)  # Ovo vraca listu produkata
                                                                             # koji su nekad bili u korpi
                                                                             # (ne mora da znaci da su zavrsili u porudzbini)
        Order = apps.get_model('orders', 'Order')
        # print(product_obj.id)
        print(Order.objects.get_by_cart_product(cart_products_obj))
        # print(str(Order.objects.get_by_product(product_obj).query))
        for p in self.products.all():
            if p.product == product_obj:
                p.quantity = product_quantity
                p.save()
                self.save()

                data = {
                    'total_weight': self.total_weight,
                    'total_price': self.total_price
                }

        return data


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
