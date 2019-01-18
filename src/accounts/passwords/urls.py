from django.conf.urls import url
from django.contrib.auth import views as auth_views

urlpatterns = [
    url('password/change/', auth_views.PasswordChangeView.as_view(), name='password_change'),
    url('password/change/done/', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),
    url('password/reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    url('password/reset/done', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    url('password/reset/(?P<uidb64>[0-9A-Za-z_\-]+)(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/',
        auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    url('password/reset/complete', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]