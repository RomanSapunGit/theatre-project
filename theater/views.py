from django.shortcuts import render
from rest_framework import mixins
from rest_framework.viewsets import ModelViewSet, GenericViewSet

from theater.models import Actor, Genre, Play, Performance
from theater.serializers import ActorSerializer, GenreSerializer, PlayDetailSerializer, PlaySerializer, \
    PerformanceDetailSerializer, PerformanceSerializer


# Create your views here.
class ActorViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    GenericViewSet
):
    queryset = Actor.objects.all()
    serializer_class = ActorSerializer


class GenreViewSet(ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class PlayViewSet(ModelViewSet):
    queryset = Play.objects.all()

    def get_serializer_class(self):
        if self.action == "retrieve":
            return PlayDetailSerializer
        return PlaySerializer


class PerformanceViewSet(ModelViewSet):
    queryset = Performance.objects.all()
    serializer_class = GenreSerializer

    def get_serializer_class(self):
        if self.action == "retrieve":
            return PerformanceDetailSerializer
        return PerformanceSerializer
