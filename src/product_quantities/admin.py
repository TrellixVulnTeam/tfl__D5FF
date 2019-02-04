from django.contrib import admin

from .models import ProductQuantity


class ProductQuantityAdmin(admin.ModelAdmin):
    list_display = ['cart', 'product', 'quantity']

    class Meta:
        model = ProductQuantity


admin.site.register(ProductQuantity, ProductQuantityAdmin)
