from django.contrib import messages
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.http import Http404, JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator

from carts.models import Cart
from .models import Product, ProductCategory, CartProduct
from .forms import ProductForm


class ProductListView(ListView):
    # queryset = Product.objects.all()
    template_name = "products/list.html"
    paginate_by = 12

    def get_queryset(self, *args, **kwargs):
        user = self.request.user
        id = self.kwargs.get('company')

        companies_menu = self.request.session['companies_menu']
        companies_ids = []
        found = False
        for c in companies_menu:
            if c['id'] == id:
                found = True
            companies_ids.append(c['id'])

        if id is not None and found:
            # return Product.objects.get_by_company(id_company=id, user=user)
            return Product.objects.get_by_company(id_company=id)
        # print(companies_ids)
        # return Product.objects.all(user, companies_ids)
        return Product.objects.all_by_companies(user, companies_ids)

    def get_context_data(self, *args, **kwargs):
        context = super(ProductListView, self).get_context_data(*args, **kwargs)
        products = self.get_queryset(*args, **kwargs)

        # p = Paginator(Product.objects.select_related().all(), self.paginate_by)
        p = Paginator(products, self.paginate_by)
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
    # queryset = Product.objects.all()
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


class ProductDetailUpdateView(LoginRequiredMixin, UpdateView):
    form_class = ProductForm
    template_name = 'products/add.html'

    def get_object(self, queryset=None):
        user = self.request.user
        product_slug = self.kwargs.get('slug')

        if user.is_staff or user.is_admin:
            if product_slug is not None:
                try:
                    product = Product.objects.get(slug=product_slug)
                    return product
                except Product.DoesNotExist:
                    raise Http404("Product doesn't exist!")

    def get_success_url(self, **kwargs):
        messages.success(self.request, 'Change successful!')
        product_slug = self.kwargs.get('slug')
        succ_url = 'products:detail'

        if product_slug is not None:
            succ_url = 'products:edit'
            if kwargs is not None:
                return reverse(succ_url, kwargs={'slug': product_slug})
            else:
                return reverse(succ_url, args=(product_slug,))

        return reverse(succ_url)


class ProductAddView(LoginRequiredMixin, CreateView):
    form_class = ProductForm
    template_name = 'products/add.html'

    model = Product


@csrf_exempt
def cart_add(request, slug=None):
    product_id = request.POST.get('product_id')
    data = {
        'refresh': 'false'
    }
    if product_id is not None:
            product_obj = Product.objects.get(id=product_id)
            cart_obj, new_obj = Cart.objects.new_or_get(request)
            find = False
            for p in cart_obj.products.all():
                if p.product == product_obj:
                    find = True
            if not find:
                cart_product = CartProduct.objects.new(product=product_obj)
                cart_obj.products.add(cart_product)
                cart_count = cart_obj.products.count()
                request.session['cart_items'] = cart_count
                data = {
                    'cart_count': cart_count,
                    'refresh': 'true'
                }

    return JsonResponse(data)
