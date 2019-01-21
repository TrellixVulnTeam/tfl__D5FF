from django.urls import path, re_path

from .views import (
        AccountHomeView,
        AccountUsernameActivateView
)

app_name = 'account'

urlpatterns = [
    path('', AccountHomeView.as_view(), name='home'),
    re_path('username/confirm/(?P<key>[0-9A-Za-z]+)/', AccountUsernameActivateView.as_view(), name='username_activate'),
]
