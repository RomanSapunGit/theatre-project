from django.shortcuts import render
from rest_framework import mixins
from rest_framework.viewsets import ModelViewSet, GenericViewSet

from theater.models import Actor, Genre, Play, Performance, Ticket, Reservation
from theater.serializers import ActorSerializer, GenreSerializer, PlayDetailSerializer, PlaySerializer, \
    PerformanceDetailSerializer, PerformanceSerializer, TicketSerializer, TicketDetailSerializer, ReservationSerializer


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

    def get_serializer_class(self):
        if self.action == "retrieve":
            return PerformanceDetailSerializer
        return PerformanceSerializer


class TicketViewSet(ModelViewSet):
    queryset = Ticket.objects.all()

    def get_serializer_class(self):
        if self.action == "retrieve":
            return TicketDetailSerializer
        return TicketSerializer


class ReservationViewSet(ModelViewSet):
    queryset = Reservation.objects.all()

    def get_serializer_class(self):
        return ReservationSerializer

