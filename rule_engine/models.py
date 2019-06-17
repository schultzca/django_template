from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class TimeStampedMixin(models.Model):
    created_by = models.ForeignKey(User, on_delete=models.PROTECT)
    created_at = models.DateTimeField(editable=False)
    updated_at = models.DateTimeField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.id:
            self.created_at = timezone.now()
        self.updated_at = timezone.now()
        return super(TimeStampedMixin, self).save(*args, **kwargs)

    class Meta:
        abstract = True


class ElasticInstance(TimeStampedMixin):
    host = models.CharField(null=False, blank=False, max_length=200)
    port = models.IntegerField(default=9200, null=False, blank=False)
    description = models.CharField(null=False, blank=False, max_length=200)
    username = models.CharField(default="", max_length=50)
    password = models.CharField(default="", max_length=50)
    cafile = models.CharField(default="", max_length=50)

    def __str__(self):
        return f"{self.host}:{self.port} - {self.description}"

    def requires_auth(self):
        return self.username or self.password

    def requires_ssl(self):
        return self.cafile

    class Meta:
        unique_together = [['host', 'port']]


class TagSet(TimeStampedMixin):
    name = models.CharField(null=False, blank=False, max_length=200)
    description = models.CharField(default="", max_length=200)

    def __str__(self):
        return f"{self.name} - {self.created_by}"


class Tag(TimeStampedMixin):
    name = models.CharField(null=False, blank=False, max_length=200)
    description = models.CharField(default="", max_length=200)
    tagset = models.ForeignKey(TagSet, on_delete=models.PROTECT)

    def __str__(self):
        return f"{self.tagset.name} - {self.name} - {self.created_by}"


class Query(TimeStampedMixin):
    query = models.CharField(null=False, blank=False, max_length=1000)
    tag = models.ForeignKey(Tag, on_delete=models.PROTECT)
    read_only = models.BooleanField(default=False, blank=False, null=False)

    class Meta:
        unique_together = [['tag', 'query']]

    def __str__(self):
        return f"{self.tag.name} - {self.created_by.username} - {self.query}"



