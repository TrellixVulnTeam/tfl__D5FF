from django.urls import path

from .views import CompanyView, CompanyAddView

app_name = 'companies'

urlpatterns = [
    path('', CompanyView.as_view(), name='home'),
    path('add/', CompanyAddView.as_view(), name='add'),
]