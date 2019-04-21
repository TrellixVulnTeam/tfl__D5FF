import random
import os
from django.db import models
from django.db.models import Q
from django.db.models.signals import pre_save, post_save
from django.urls import reverse

from tfl.utils import unique_slug_generator
from companies.models import Company


def get_filename_ext(filepath):
    base_name = os.path.basename(filepath)
    name, ext = os.path.splitext(base_name)
    return name, ext


def upload_image_path(instance, filename):
    new_filename = random.randint(1, 3265456541)
    name, ext = get_filename_ext(filename)
    final_name = '{new_filename}{ext}'.format(new_filename=new_filename, ext=ext)
    return 'products/{new_filename}/{final_name}'.format(
        new_filename=new_filename,
        final_name=final_name
    )


class ProductCategoryQuerySet(models.query.QuerySet):
    def active(self):
        return self.filter(active=True)


class ProductCategoryManager(models.Manager):
    def get_queryset(self):
        return ProductCategoryQuerySet(self.model, using=self._db)

    def get_by_id(self, id):
        qs = self.get_queryset().filter(id=id)
        if qs.count() == 1:
            return qs.first()
        return None

    def all(self):
        return self.get_queryset().active()


class ProductCategory(models.Model):
    name = models.CharField(max_length=256)
    active = models.BooleanField(default=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    objects = ProductCategoryManager()

    def __str__(self):
        return self.name


class ProductQuerySet(models.query.QuerySet):
    def all(self, companies_ids):
        print(companies_ids)
        return self.filter(company__in=companies_ids).filter(active=True).order_by('-timestamp')

    def get_by_company(self, id_company):
        return self.filter(Q(company=id_company)).order_by('-timestamp')

    def search_cq(self, category, query):
        lookups = ((Q(title__icontains=query) |
                   Q(description__icontains=query) |
                   Q(price__icontains=query) |
                   Q(tag__title__icontains=query)) &
                   Q(category=category)
                   )
        return self.filter(lookups).order_by('-timestamp').distinct()

    def search_c(self, category):
        return self.filter(Q(category=category)).order_by('-timestamp')

    def search_q(self, query):
        lookups = (Q(title__icontains=query) |
                   Q(description__icontains=query) |
                   Q(price__icontains=query) |
                   Q(tag__title__icontains=query)
                   )
        return self.filter(lookups).order_by('-timestamp').distinct()


class ProductManager(models.Manager):
    def get_queryset(self):
        return ProductQuerySet(self.model, using=self._db)

    def all(self, user, companies_ids):
        # if user.is_authenticated:
        #     if user.is_staff or user.is_admin:
                return self.get_queryset().all(companies_ids)
            # else:
            #     return self.get_by_company(id_company=user.company, user=user)
        # return None

    def get_by_id(self, id):
        qs = self.get_queryset().filter(id=id)
        if qs.count() == 1:
            return qs.first()
        return None

    # def get_by_company(self, id_company, user):
    #     if user.is_staff or user.is_admin:
    #         return self.get_queryset().active().get_by_company(id_company=id_company)
    #     else:
    #         return self.get_queryset().active().get_by_company(id_company=user.company)
    def get_by_company(self, id_company, user):
        return self.get_queryset().get_by_company(id_company=id_company)

    def search(self, category, query, companies_ids):
        if category and query:
            return self.get_queryset().all(companies_ids).search_cq(category, query)
        elif category:
            return self.get_queryset().all(companies_ids).search_c(category)
        else:
            return self.get_queryset().all(companies_ids).search_q(query)


class Product(models.Model):
    title = models.CharField(max_length=120)
    slug = models.SlugField(blank=True, unique=True)
    description = models.TextField()
    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True)
    price = models.DecimalField(decimal_places=2, max_digits=20, default=0.00)
    weight = models.DecimalField(decimal_places=2, max_digits=20, default=0.00)
    location = models.CharField(max_length=120, default='-')
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE, null=True) #problem
    quantity = models.IntegerField(default=0, blank=False, null=False)
    image = models.ImageField(upload_to=upload_image_path, default='products/no-image.jpg')
    active = models.BooleanField(default=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    objects = ProductManager()

    def get_absolute_url(self):
        return reverse('products:detail', kwargs={'slug': self.slug})

    def __str__(self):
        return self.title


def product_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)


pre_save.connect(product_pre_save_receiver, sender=Product)


class CartProductManager(models.Manager):
    def new(self, product):
        product_obj = product
        return self.model.objects.create(product=product_obj)


class CartProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    updated = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    objects = CartProductManager()

    def __str__(self):
        return str(self.id)

    # class Meta:
    #     unique_together = (('cart', 'product'),)
