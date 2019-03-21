from django.db import models
from django.urls import reverse


class CompanyQuerySet(models.query.QuerySet):
    def active(self):
        return self.filter(active=True).order_by('-timestamp')


class CompanyManager(models.Manager):
    def get_queryset(self):
        return CompanyQuerySet(self.model, using=self._db)

    def active(self):
        return self.get_queryset().active()

    def get_by_id(self, id):
        qs = self.get_queryset().filter(id=id)
        if qs.count() == 1:
            return qs.first()
        return None

    def all(self):
        return self.get_queryset().order_by('-timestamp')


class Company(models.Model):
    name = models.CharField(max_length=120)
    active = models.BooleanField(default=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    objects = CompanyManager()

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('companies:home')
