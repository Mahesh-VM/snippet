from rest_framework.routers import DefaultRouter
from snippetapp.viewsets import (
    TagViewSet,
    SnippetViewSet,
    OverviewViewSet,
)
from django.urls import path, include


router = DefaultRouter(trailing_slash=False)
router.register("tag", TagViewSet)
router.register("snippet", SnippetViewSet)
router.register("overview", OverviewViewSet, 'overview')


urlpatterns = [
    path('', include(router.urls)),
]