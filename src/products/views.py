from django.views.generic import ListView, DetailView, CreateView
from django.http import Http404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator

from .models import Product, ProductCategory
from .forms import ProductForm


class ProductListView(ListView):
    # queryset = Product.objects.all()
    template_name = "products/list.html"
    paginate_by = 12

    def get_queryset(self, *args, **kwargs):
        # request = self.request
        return Product.objects.all()

    def get_context_data(self, *args, **kwargs):
        context = super(ProductListView, self).get_context_data(*args, **kwargs)
        p = Paginator(Product.objects.select_related().all(), self.paginate_by)
        context['products'] = p.page(context['page_obj'].number)
        all_categories = ProductCategory.objects.all()
        context['all_categories'] = all_categories

        return context

# def product_list_view(request):
#     queryset = Product.objects.all()
#     context = {
#         'qs': queryset
#     }
#     return render(request, "product/list.html", context)


# class ProductDetailView(DetailView):
#     template_name = "products/detail.html"
#
#     def get_context_data(self, *args, **kwargs):
#         context = super(ProductDetailView, self).get_context_data(*args, **kwargs)
#         return context
#
#     def get_object(self, *args, **kwargs):
#         request = self.request
#         pk = self.kwargs.get('pk')
#         instance = Product.objects.get_by_id(pk)
#         if instance is None:
#             raise Http404("Product doesn't exist!")
#         return instance

class ProductDetailView(DetailView):
    queryset = Product.objects.all()
    template_name = "products/detail.html"

    # def get_context_data(self, *args, **kwargs):
    #     context = super(ProductDetailView, self).get_context_data(*args, **kwargs)
    #     return context

    def get_object(self, *args, **kwargs):
        request = self.request
        slug = self.kwargs.get('slug')
        # instance = Product.objects.get_by_id(slug)
        # if instance is None:
        #    raise Http404("Product doesn't exist!")
        # return instance
        try:
            instance = Product.objects.get(slug=slug, active=True)
        except Product.DoesNotExist:
            raise Http404("Product doesn't exist!")
        except Product.MultipleObjectsReturned:
            qs = Product.objects.filter(slug=slug, active=True)
            instance = qs.first()
        except:
            raise Http404("Uhhh")
        return instance


class ProductAddView(LoginRequiredMixin, CreateView):
    form_class = ProductForm
    template_name = 'products/add.html'

    model = Product
