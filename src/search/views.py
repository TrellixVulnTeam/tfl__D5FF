from django.shortcuts import render
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin

from products.models import Product, ProductCategory


class SearchProductView(LoginRequiredMixin, ListView):
    template_name = "search/view.html"

    def get_context_data(self, *args, **kwargs):
        context = super(SearchProductView, self).get_context_data(*args, **kwargs)
        category_obj = None
        query = self.request.GET.get('q')
        category_id = self.request.GET.get('c')

        if category_id is not None and category_id != '':
            category_obj = ProductCategory.objects.get_by_id(category_id)

        all_categories = ProductCategory.objects.all()
        context['query'] = query
        context['category'] = category_obj
        context['all_categories'] = all_categories
        return context

    def get_queryset(self, *args, **kwargs):
        request = self.request
        user = request.user
        query = request.GET.get('q')
        category = request.GET.get('c')

        companies_menu = request.session['companies_menu']
        companies_ids = []
        for c in companies_menu:
            companies_ids.append(c['id'])
        if not query and not category:
            return Product.objects.all_by_companies(user, companies_ids)
        else:
            return Product.objects.search(category, query, companies_ids)
