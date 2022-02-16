from rest_framework.viewsets import ModelViewSet
from snippetapp.models import (
    Tag,
    Snippet,
)
from snippetapp.serializers import (
    TagSerializer,
    SnippetSerializer,
    OverviewSerializer,
)
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from rest_framework.permissions import IsAuthenticated


class TagViewSet(ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    http_method_names = ('get',)
    permission_classes = (IsAuthenticated,)

    def retrieve(self, request, *args, **kwargs):
        print(self.request.user)
        instance = self.get_object()
        snippets = Snippet.objects.filter(tag__title=instance)
        serializer = SnippetSerializer(snippets, many=True)
        return Response(serializer.data)


class SnippetViewSet(ModelViewSet):
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer
    http_method_names = ('get', 'post', 'put', 'patch', 'delete')
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def perform_update(self, serializer):
        serializer.save(owner=self.request.user)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=HTTP_200_OK)


class OverviewViewSet(ModelViewSet):
    queryset = Snippet.objects.all()
    serializer_class = OverviewSerializer
    http_method_names = ('get',)
    permission_classes = (IsAuthenticated,)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        data = serializer.data
        res = dict()
        res['count'] = len(queryset)
        res['data'] = data
        return Response(res)
