from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.generic import TemplateView
from django.views.decorators.csrf import csrf_exempt

from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search

from rule_engine.models import ElasticInstance, TagSet, Tag, Query


class QueryCreationView(TemplateView):

    template_name = "rule_engine/query_creation"

    def get(self, request, *args, **kwargs):
        return render(request, self.get_template_names(),
                      context={"instances": ElasticInstance.objects.all(),
                               "tagsets": TagSet.objects.all()})


def indices(request):
    """Ajax request that queries Elasticsearch and returns the list of
    indices that exist."""
    elastic_instance = request.GET.get("instance", None)

    client = Elasticsearch(hosts=[elastic_instance])
    data = {
        "indices": client.indices.get_alias("*")
    }

    return JsonResponse(data=data)


def search(request):
    """Ajax request that runs a query string sent in request against Elasticsearch index
    and returns the raw results.
    """
    elastic_instance = request.GET.get("instance", None)
    elastic_index = request.GET.get("index", None)
    query_string = request.GET.get("query_string", None)

    client = Elasticsearch(hosts=[elastic_instance])
    results = Search(using=client, index=elastic_index).query("query_string", query=query_string).execute()

    return JsonResponse(results.to_dict())


@csrf_exempt
def create_query(request):
    """Ajax request for creating a new query."""
    Query(
        tag=Tag.objects.get(id=int(request.POST["tag_id"])),
        query=request.POST["query_string"],
        created_by=request.user
    ).save()
    return HttpResponse(status=201)


@csrf_exempt
def delete_query(request):
    """Ajax request for deleting an existing query."""
    query = Query.objects.get(id=request.POST["query_id"])
    if query.read_only:
        return HttpResponse(status=403)
    elif query.created_by == request.user:
        query.delete()
    return HttpResponse(status=200)
