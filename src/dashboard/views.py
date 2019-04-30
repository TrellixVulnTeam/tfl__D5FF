import json

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model
from django.core.serializers import serialize
from django.core.serializers.json import DjangoJSONEncoder
from django.views.generic import TemplateView
from django.http import JsonResponse

from rest_framework.views import APIView
from rest_framework.response import Response

from companies.models import Company
from products.models import Product
from orders.models import Order


User = get_user_model()


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard/home.html'


class DashboardDataApiView(LoginRequiredMixin, APIView):

    # Users Company
    def users_company_data(self):
        all_companies = Company.objects.all()
        companies_name = []
        companies_users = []

        for c in all_companies:
            companies_name.append(c.name)
            users_num = User.objects.get_users_by_company(company_id=c.id).count()
            companies_users.append(users_num)

        companies_name.append("No Company")
        users_num = User.objects.get_users_by_company(company_id=None).count()
        companies_users.append(users_num)

        data = {
            "companies_name": companies_name,
            "companies_users": companies_users,
        }

        return JsonResponse(data)

    # Active and Inactive Users
    def active_inactive_users(self):
        users_num = []
        active_users = User.objects.active().count()
        inactive_users = User.objects.inactive().count()

        users_num.append(active_users)
        users_num.append(inactive_users)

        data = {
            "labels": ["Active", "Inactive"],
            "users_num": users_num
        }

        return JsonResponse(data)

    # Company Products
    def companies_products(self):
        all_companies = Company.objects.all()
        companies_name = []
        companies_products = []

        for c in all_companies:
            companies_name.append(c.name)
            product_num = Product.objects.get_by_company(id_company=c.id).count()
            companies_products.append(product_num)

        data = {
            "companies_name": companies_name,
            "companies_products": companies_products,
        }

        return JsonResponse(data)

    # Company Orders
    def companies_orders(self):
        all_companies = Company.objects.all()
        companies_name = []
        companies_orders = []

        for c in all_companies:
            companies_name.append(c.name)
            order_num = Order.objects.get_by_company(company=c.id).count()
            companies_orders.append(order_num)

        data = {
            "companies_name": companies_name,
            "companies_orders": companies_orders,
        }

        return JsonResponse(data)

    def get(self, request, format=None):
        data = {
            "users_company_data": self.users_company_data().content,
            "active_inactive_users": self.active_inactive_users().content,
            "companies_products": self.companies_products().content,
            "companies_orders": self.companies_orders().content
        }

        return Response(data)
