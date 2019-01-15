from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin
)


class UserManager(BaseUserManager):
    def create_user(self, email, personal_name, password=None, is_active=False, is_staff=False, is_admin=False):
        if not email:
            raise ValueError('Users must have an email address')
        if not password:
            raise ValueError('Users mast have a password')
        if not personal_name:
            raise ValueError('Users mast have a personal name')

        user_obj = self.model(
            email = self.normalize_email(email),
            personal_name = personal_name
        )
        user_obj.set_password(password)
        user_obj.staff = is_staff
        user_obj.admin = is_admin
        user_obj.active = is_active
        user_obj.save(using=self._db)

        return user_obj

    def create_staffuser(self, email, personal_name, password):
        user = self.create_user(
            email,
            personal_name,
            password=password,
            is_staff=True,
            is_active=True
        )

        return user

    def create_superuser(self, email, personal_name, password):
        user = self.create_user(
            email,
            personal_name,
            password=password,
            is_staff=True,
            is_admin=True,
            is_active=True
        )

        return user


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=255, unique=True)
    personal_name = models.CharField(max_length=255, blank=True, null=True)
    active = models.BooleanField(default=False)
    staff = models.BooleanField(default=False)
    admin = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = ['personal_name']

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.admin

    def has_module_perms(self, app_label):
        return self.admin

    @property
    def is_staff(self):
        return self.staff

    @property
    def is_admin(self):
        return self.admin

    @property
    def is_active(self):
        return self.active

