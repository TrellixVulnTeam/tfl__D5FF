from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin
)


class UserManager(BaseUserManager):
    def create_user(self, email, username, personal_name=None, address=None, phone=None, password=None, is_active=False, is_staff=False, is_admin=False):
        if not email:
            raise ValueError('Users must have an email address')
        if not username:
            raise ValueError('Users must have a username')
        if not password:
            raise ValueError('Users mast have a password')

        user_obj = self.model(
            email=self.normalize_email(email),
            personal_name=personal_name,
            username=username,
            address=address,
            phone=phone
        )

        user_obj.set_password(password)
        user_obj.staff = is_staff
        user_obj.admin = is_admin
        user_obj.active = is_active
        user_obj.save(using=self._db)

        return user_obj

    def create_staffuser(self, email, username, personal_name, address, phone, password):
        user = self.create_user(
            email,
            username,
            personal_name,
            address,
            phone,
            password=password,
            is_staff=True,
            is_active=True
        )

        return user

    def create_superuser(self, email, username, personal_name, address, phone, password):
        user = self.create_user(
            email,
            username,
            personal_name,
            address,
            phone,
            password=password,
            is_staff=True,
            is_admin=True,
            is_active=True
        )

        return user


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=255, unique=True)
    username = models.CharField(max_length=255, unique=True)
    personal_name = models.CharField(max_length=255, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    phone = models.CharField(max_length=255, blank=True, null=True)
    active = models.BooleanField(default=False)
    staff = models.BooleanField(default=False)
    admin = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    objects = UserManager()

    USERNAME_FIELD = 'username'

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

