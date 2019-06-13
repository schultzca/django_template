from django.http import JsonResponse
from django.shortcuts import render
from django.views.generic import View, TemplateView

from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search

from rule_engine.models import ElasticInstance, TagSet


class HomeView(TemplateView):

    template_name = "rule_engine/home.html"


class SearchView(TemplateView):

    template_name = "rule_engine/search.html"

    def get(self, request, *args, **kwargs):
        return render(request, self.get_template_names(),
                      context={"instances": ElasticInstance.objects.all(),
                               "tagsets": TagSet.objects.all()})


def indices(request):

    elastic_instance = request.GET.get("instance", None)

    client = Elasticsearch(hosts=[elastic_instance])
    data = {
        "indices": client.indices.get_alias("*")
    }

    return JsonResponse(data=data)


def search(request):

    elastic_instance = request.GET.get("instance", None)
    elastic_index = request.GET.get("index", None)
    query_string = request.GET.get("query_string", None)

    client = Elasticsearch(hosts=[elastic_instance])
    results = Search(using=client, index=elastic_index).query("query_string", query=query_string).execute()

    return JsonResponse(results.to_dict())

