from django.contrib import admin

from .models import Company


class CompanyAdmin(admin.ModelAdmin):
    list_display = ['__str__']

    class Meta:
        model = Company


admin.site.register(Company, CompanyAdmin)
