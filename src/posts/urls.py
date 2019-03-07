from django.urls import path

from .views import (
    PostView,
    post_add
)

app_name = 'post'

urlpatterns = [
    path('', PostView.as_view(), name='home'),
    path('add/', post_add, name='add'),
]
