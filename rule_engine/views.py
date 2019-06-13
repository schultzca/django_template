from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.generic import TemplateView
from django.views.decorators.csrf import csrf_exempt

from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search

from rule_engine.models import ElasticInstance, TagSet, Tag, Query


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


@csrf_exempt
def create_query(request):
    Query(
        tag=Tag.objects.get(id=int(request.POST["tag_id"])),
        query=request.POST["query_string"],
        created_by=request.user
    ).save()
    return HttpResponse(status=201)


@csrf_exempt
def delete_query(request):
    query = Query.objects.get(id=request.POST["query_id"])
    if query.read_only:
        return HttpResponse(status=403)
    else:
        query.delete()
    return HttpResponse(status=200)
