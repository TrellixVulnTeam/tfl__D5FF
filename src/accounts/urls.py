from django.urls import path, re_path

from .views import (
        AccountHomeView,
        AccountUsernameActivateView,
        UserDetailUpdateView
)

app_name = 'account'

urlpatterns = [
    path('', UserDetailUpdateView.as_view(), name='home'),
    # path('details/', UserDetailUpdateView.as_view(), name='user_update'),
    re_path('username/confirm/(?P<key>[0-9A-Za-z]+)/', AccountUsernameActivateView.as_view(), name='username_activate'),
    re_path('username/resend_activation/', AccountUsernameActivateView.as_view(), name='resend_activation'),
]
