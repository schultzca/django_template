from rest_framework import routers, serializers, viewsets

import rule_engine.models as models


class TagSetSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.TagSet
        fields = '__all__'


class TagSetViewSet(viewsets.ModelViewSet):
    queryset = models.TagSet.objects.all()
    serializer_class = TagSetSerializer


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Tag
        fields = '__all__'


class TagViewSet(viewsets.ModelViewSet):
    queryset = models.Tag.objects.all()
    serializer_class = TagSerializer

    def get_queryset(self):
        tagset_id = self.request.GET.get("tagset_id", None)
        if tagset_id is None:
            return self.queryset
        return models.Tag.objects.filter(
            tagset=models.TagSet.objects.get(id=int(tagset_id)))


class QuerySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Query
        fields = '__all__'


class QueryViewSet(viewsets.ModelViewSet):
    queryset = models.Query.objects.all()
    serializer_class = QuerySerializer

    def get_queryset(self):
        tag_id = self.request.GET.get("tag_id", None)
        print(tag_id)
        if tag_id is None:
            return self.queryset
        return models.Query.objects.filter(tag=models.Tag.objects.get(id=int(tag_id)))


router = routers.DefaultRouter()
router.register('tagsets', TagSetViewSet)
router.register('tags', TagViewSet)
router.register('queries', QueryViewSet)
