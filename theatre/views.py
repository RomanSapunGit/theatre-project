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

    def get_queryset(self):
        first_name = self.request.query_params.get("first_name")
        last_name = self.request.query_params.get("last_name")

        queryset = self.queryset

        if first_name:
            queryset = queryset.filter(first_name__icontains=first_name)

        if last_name:
            queryset = queryset.filter(last_name__icontains=last_name)

        return queryset.distinct()


class GenreViewSet(ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer

    def get_queryset(self):
        name = self.request.query_params.get("name")

        queryset = self.queryset

        if name:
            queryset = queryset.filter(name__icontains=name)

        return queryset.distinct()

class PlayViewSet(ModelViewSet):
    queryset = Play.objects.all()

    def get_serializer_class(self):
        if self.action == "retrieve":
            return PlayDetailSerializer
        if self.action == "list":
            return PlayListSerializer
        if self.action == "upload_image":
            return PlayImageSerializer
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


class TheatreHallViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    GenericViewSet,
):
    queryset = TheatreHall.objects.all()
    serializer_class = TheatreHallSerializer
