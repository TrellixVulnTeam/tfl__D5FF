"""tfl URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static

from django.contrib import admin
from django.contrib.auth.views import LogoutView
from django.urls import path, include

from .views import home_page
from accounts.views import LoginView, RegisterView
from products.views import ProductAddView
from dashboard.views import DashboardView, ChartDataView


urlpatterns = [
    path('', include('posts.urls', namespace='post')),
    path('account/', include('accounts.urls', namespace='account')),
    path('accounts/', include('accounts.passwords.urls')),
    path('add_product/', ProductAddView.as_view(), name='add_product'),
    path('cart/', include('carts.urls', namespace='cart')),
    path('companies/', include('companies.urls', namespace='companies')),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('api/dashboard/', ChartDataView.as_view(), name='dashboard-api'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('orders/', include('orders.urls', namespace='orders')),
    path('register/', RegisterView.as_view(), name='register'),
    path('products/', include('products.urls', namespace='products')),
    path('search/', include('search.urls', namespace='search')),
    path('admin/', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns = urlpatterns + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
