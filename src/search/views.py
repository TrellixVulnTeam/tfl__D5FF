from django.shortcuts import render
from django.views.generic import ListView

from products.models import Product, ProductCategory


class SearchProductView(ListView):
    template_name = "search/view.html"

    def get_context_data(self, *args, **kwargs):
        context = super(SearchProductView, self).get_context_data(*args, **kwargs)
        query = self.request.GET.get('q')
        # category = self.request.GET.get('c')
        all_categories = ProductCategory.objects.all()
        context['query'] = query
        context['all_categories'] = all_categories
        return context

    def get_queryset(self, *args, **kwargs):
        request = self.request
        user = self.request.user
        query = request.GET.get('q')
        category = request.GET.get('c')

        if not query and not category:
            return Product.objects.all(user)
        else:
            return Product.objects.search(category, query)
