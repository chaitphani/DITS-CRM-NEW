from django.db import models
from django.db.models.query import QuerySet
from .choices import ObjectStatusChoices
from django.utils.text import slugify

class SoftDeletionQuerySet(QuerySet):
    def delete(self):
        return super(SoftDeletionQuerySet, self).update(object_status=ObjectStatusChoices.DELETED)

    def hard_delete(self):
        return super(SoftDeletionQuerySet, self).delete()

class ObjectManager(models.Manager):
    def get_queryset(self):
        return SoftDeletionQuerySet(self.model).filter(object_status=ObjectStatusChoices.ACTIVE)

    def complete(self):
        return super().get_queryset()


class BaseModel(models.Model):

    added_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    object_status = models.SmallIntegerField(choices=ObjectStatusChoices.CHOICES, default=ObjectStatusChoices.ACTIVE)
    objects = ObjectManager()

    class Meta:
        abstract = True


class Country(models.Model):
    country_code = models.CharField(max_length=5)
    name = models.CharField(max_length=255)
    slug = models.SlugField(null=True, blank=True, editable=False, max_length=500)

    def __str__(self):
        return "{0}".format(self.name)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Country, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = "Countries"
