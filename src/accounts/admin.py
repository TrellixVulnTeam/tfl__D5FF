from django.contrib import admin
from django.contrib.auth import get_user_model

from .models import UsernameActivation

User = get_user_model()


class UserAdmin(admin.ModelAdmin):
    search_fields = ['username']

    class Meta:
        model = User


admin.site.register(User, UserAdmin)


class UsernameActivationAdmin(admin.ModelAdmin):
    search_fields = ['username']

    class Meta:
        model = UsernameActivation


admin.site.register(UsernameActivation, UsernameActivationAdmin)


