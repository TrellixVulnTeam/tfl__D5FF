from django.urls import path, re_path

from .views import (
        AccountHomeView,
        AccountUsernameActivateView,
        UserDetailUpdateView,
        AllUsersView
)

app_name = 'account'

urlpatterns = [
    path('', UserDetailUpdateView.as_view(), name='home'),
    path('all/', AllUsersView.as_view(), name='all'),
    path('all/user-<slug:id>', UserDetailUpdateView.as_view(), name='user_detail'),
    re_path('username/confirm/(?P<key>[0-9A-Za-z]+)/', AccountUsernameActivateView.as_view(), name='username_activate'),
    re_path('username/resend_activation/', AccountUsernameActivateView.as_view(), name='resend_activation'),
]
