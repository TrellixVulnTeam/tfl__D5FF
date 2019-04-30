import random
import os
from django.conf import settings
from django.db import models


User = settings.AUTH_USER_MODEL


def get_filename_ext(filepath):
    base_name = os.path.basename(filepath)
    name, ext = os.path.splitext(base_name)
    return name, ext


def upload_image_path(instance, filename):
    new_filename = random.randint(1, 3265456541)
    name, ext = get_filename_ext(filename)
    final_name = '{new_filename}{ext}'.format(new_filename=new_filename, ext=ext)
    return 'posts/{new_filename}/{final_name}'.format(
        new_filename=new_filename,
        final_name=final_name
    )


class PostQuerySet(models.query.QuerySet):
    def active(self):
        return self.filter(active=True).order_by('-timestamp')


class PostManager(models.Manager):
    def get_queryset(self):
        return PostQuerySet(self.model, using=self._db)

    def all(self):
        return self.get_queryset().active()

    def get_by_id(self, id):
        qs = self.get_queryset().filter(id=id)
        if qs.count() == 1:
            return qs.first()
        return None

    def new(self, form, user=None):
        user_obj = None
        if user is not None:
            if user.is_authenticated:
                user_obj = user
                image = form.cleaned_data['image']
                description = form.cleaned_data['description']
                return self.model.objects.create(user=user_obj, description=description, image=image)
        return None

    def remove(self, post_id):
        if post_id is not None and post_id != '':
            post_obj = self.get_by_id(post_id)
            if post_obj is not None:
                post_obj.active = False
                post_obj.save()


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    description = models.CharField(max_length=2048, blank=True, null=True)
    image = models.ImageField(upload_to=upload_image_path, blank=True, null=True)
    updated = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)

    objects = PostManager()

    def __str__(self):
        return str(self.id)
