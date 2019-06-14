"""webapps URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, include
from rule_engine import views

urlpatterns = [
    path("", views.QueryCreationView.as_view(), name="Search"),
    path("ajax/indices/", views.indices),
    path("ajax/search/", views.search),
    path("ajax/create_query/", views.create_query),
    path("ajax/delete_query/", views.delete_query),
    path("api/", include('rule_engine.api.urls'))
]
