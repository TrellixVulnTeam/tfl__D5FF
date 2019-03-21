from django.views.generic import CreateView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Company
from .forms import CompanyForm


class CompanyView(LoginRequiredMixin, ListView):
    template_name = 'companies/home.html'

    def get_queryset(self):
        return Company.objects.all()

    def get_context_data(self, *args, **kwargs):
        context = super(CompanyView, self).get_context_data(*args, **kwargs)
        return context


class CompanyAddView(LoginRequiredMixin, CreateView):
    form_class = CompanyForm
    template_name = 'companies/add.html'

    model = Company
