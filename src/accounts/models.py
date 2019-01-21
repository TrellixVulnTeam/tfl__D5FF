from datetime import timedelta
from django.conf import settings
from django.urls import reverse
from django.db import models
from django.db.models.signals import pre_save, post_save

from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin
)

from django.core.mail import send_mail
from django.template.loader import get_template
from django.utils import timezone

from tfl.utils import unique_key_generator

DEFAULT_ACTIVATION_DAYS = getattr(settings, 'DEFAULT_ACTIVATION_DAYS', 7)


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
        user_obj.is_active = is_active
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
    is_active = models.BooleanField(default=False)
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

    # @property
    # def is_active(self):
    #     return self.active


class UsernameActivationQuerySet(models.query.QuerySet):
    def confirmable(self):
        now = timezone.now()
        start_range = now - timedelta(days=DEFAULT_ACTIVATION_DAYS)
        end_range = now

        return self.filter(
            activated=False,
            forced_expired=False).filter(
            timestamp__gt=start_range,
            timestamp__lte=end_range
        )


class UsernameActivationManager(models.Manager):
    def get_queryset(self):
        return UsernameActivationQuerySet(self.model, using=self._db)

    def confirmable(self):
        return self.get_queryset().confirmable()


class UsernameActivation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    email = models.EmailField()
    username = models.CharField(max_length=255)
    key = models.CharField(max_length=120, blank=True, null=True)
    activated = models.BooleanField(default=False)
    forced_expired = models.BooleanField(default=False)
    expires = models.IntegerField(default=7)  # 7 days
    timestamp = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)

    objects = UsernameActivationManager()

    def __str__(self):
        return self.email

    def can_activate(self):
        qs = UsernameActivation.objects.filter(pk=self.pk).confirmable()
        if qs.exists():
            return True
        return False

    def activate(self):
        if self.can_activate():
            user = self.user
            user.is_activate = True
            user.save()
            self.activated = True
            self.save()
            return True
        return False

    def regenerate(self):
        self.key = None
        self.save()
        if self.key is not None:
            return True
        return False

    def send_activation(self):
        if not self.activated and not self.forced_expired:
            if self.key:
                base_url = getattr(settings, 'BASE_URL', '127.0.0.1:8000')
                key_path = reverse('account:username_activate', kwargs={'key': self.key})
                path = '{base}{path}'.format(base=base_url, path=key_path)
                context = {
                    'path': path,
                    'username': self.username
                }
                txt_ = get_template('registration/usernames/verify.txt').render(context)
                html_ = get_template('registration/usernames/verify.html').render(context)
                subject = 'Account Activate'
                from_email = settings.EMAIL_HOST_USER
                recipient_list = [from_email]

                sent_mail = send_mail(
                                subject,
                                txt_,
                                from_email,
                                recipient_list,
                                html_message=html_,
                                fail_silently=False
                            )
                return sent_mail
        return False


def pre_save_email_activation(sender, instance, *args, **kwargs):
    if not instance.activated and not instance.forced_expired:
        if not instance.key:
            instance.key = unique_key_generator(instance)


pre_save.connect(pre_save_email_activation, sender=UsernameActivation)


def post_save_user_create_receiver(sender, instance, created, *args, **kwargs):
    if created:
        obj = UsernameActivation.objects.create(user=instance, username=instance.username)
        obj.send_activation()


post_save.connect(post_save_user_create_receiver, sender=User)
