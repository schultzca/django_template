from django.contrib import admin

import rule_engine.models as models

# Register your models here.
admin.site.register(models.ElasticInstance)
admin.site.register(models.TagSet)
admin.site.register(models.Tag)
admin.site.register(models.Query)
