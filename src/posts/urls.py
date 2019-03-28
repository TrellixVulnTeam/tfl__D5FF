from django.urls import path

from .views import (
    PostView,
    post_add,
    post_remove
)

app_name = 'post'

urlpatterns = [
    path('', PostView.as_view(), name='home'),
    path('add/', post_add, name='add'),
    path('remove/', post_remove, name='remove'),
]
