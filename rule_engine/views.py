from functools import lru_cache
from pathlib import Path
from ssl import create_default_context

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.generic import TemplateView
from django.views.decorators.csrf import csrf_exempt

from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search

from rule_engine.models import ElasticInstance, TagSet, Tag, Query


CERTIFICATE_DIR = Path(__file__).parents[1].joinpath("certs")


class QueryCreationView(TemplateView):

    template_name = "rule_engine/query_creation.html"

    def get(self, request, *args, **kwargs):
        return render(request, self.get_template_names(),
                      context={"instances": ElasticInstance.objects.all(),
                               "tagsets": TagSet.objects.all()})


@lru_cache(maxsize=128)
def create_es_client(host, port=9200):
    instance = ElasticInstance.objects.get(host=host, port=port)

    hosts = [f"{instance.host}:{instance.port}"]
    if instance.requires_auth():
        hosts = [
            f"http://{instance.username}:{instance.password}@{instance.host}:{instance.port}",
            f"https://{instance.username}:{instance.password}@{instance.host}:{instance.port}",
        ]

    ssl_context = None
    if instance.requires_ssl():
        ssl_context = create_default_context(cafile=str(CERTIFICATE_DIR.joinpath(instance.cafile)))

    return Elasticsearch(hosts=hosts, ssl_context=ssl_context)


def indices(request):
    """Ajax request that queries Elasticsearch and returns the list of
    indices that exist."""
    host = request.GET.get("instance", None)

    client = create_es_client(host)
    data = {
        "indices": client.indices.get_alias("*")
    }

    return JsonResponse(data=data)


def search(request):
    """Ajax request that runs a query string sent in request against Elasticsearch index
    and returns the raw results.
    """
    host = request.GET.get("instance", None)
    elastic_index = request.GET.get("index", None)
    query_string = request.GET.get("query_string", None)

    client = create_es_client(host)
    results = Search(using=client, index=elastic_index).query("query_string", query=query_string)[0:10000].execute()

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
    elif query.created_by == request.user or request.user.is_superuser:
        query.delete()
    return HttpResponse(status=200)
