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

    def __str__(self):
        return f"{self.host}:{self.port} - {self.description}"


class TagSet(TimeStampedMixin):
    name = models.CharField(null=False, blank=False, max_length=200)

    def __str__(self):
        return self.name


class Tag(TimeStampedMixin):
    name = models.CharField(null=False, blank=False, max_length=1000)
    tagset = models.ForeignKey(TagSet, on_delete=models.PROTECT)

    def __str__(self):
        return self.name


class Query(TimeStampedMixin):
    query = models.CharField(null=False, blank=False, max_length=1500)
    tag = models.ForeignKey(Tag, on_delete=models.PROTECT)
    read_only = models.BooleanField(default=False, blank=False, null=False)

    class Meta:
        unique_together = [['tag', 'query']]

    def __str__(self):
        return self.query


class QueryOperation(TimeStampedMixin):
    query = models.ForeignKey(Query, on_delete=models.PROTECT)
    op = models.CharField(
        max_length=20,
        choices=([
            ("CREATE", "CREATE"),
            ("DELETE", "DELETE")
        ]),
        default="CREATE"
    )


