from django.urls import path, include
from rule_engine.api.views import router


urlpatterns = [
    path("", include(router.urls)),
    path("api-auth", include('rest_framework.urls', namespace='rest_framework'))
]