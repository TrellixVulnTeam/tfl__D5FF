from django.contrib import admin
from .models import Product, CartProduct, ProductCategory


class ProductAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'slug']

    class Meta:
        model = Product


admin.site.register(Product, ProductAdmin)


class CartProductAdmin(admin.ModelAdmin):
    list_display = ['__str__']

    class Meta:
        model = CartProduct


admin.site.register(CartProduct, CartProductAdmin)


class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = ['__str__']

    class Meta:
        model = ProductCategory


admin.site.register(ProductCategory, ProductCategoryAdmin)
