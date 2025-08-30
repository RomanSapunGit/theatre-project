from datetime import datetime

from django.db.models import F, Count
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, GenericViewSet

from theatre.models import (
    Actor,
    Genre,
    Play,
    Performance,
    Reservation,
    TheatreHall
)
from theatre.permissions import (
    IsAuthorizedOrIfAuthenticatedReadOnly,
    IsAdminOrIfAuthenticatedReadOnly
)
from theatre.serializers import (
    ActorSerializer,
    GenreSerializer,
    PlayDetailSerializer,
    PlaySerializer,
    PerformanceDetailSerializer,
    PerformanceSerializer,
    ReservationSerializer,
    PerformanceListSerializer,
    TheatreHallSerializer,
    ReservationListSerializer,
    PlayListSerializer,
    PlayImageSerializer
)


class ActorViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    GenericViewSet
):
    queryset = Actor.objects.all()
    serializer_class = ActorSerializer
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = ActorFilterSet

    @extend_schema(
        parameters=[
            OpenApiParameter(
                "first_name",
                type=OpenApiTypes.STR,
                description="Filter actors by "
                            "first name "
                            "(ex. ?first_name=John)",
            ),
            OpenApiParameter(
                "last_name",
                type=OpenApiTypes.STR,
                description="Filter actors by "
                            "last name "
                            "(ex. ?last_name=Doe)",
            ),
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class GenreViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    GenericViewSet,
):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = GenreFilterSet

    @extend_schema(
        parameters=[
            OpenApiParameter(
                "name",
                type=OpenApiTypes.STR,
                description="Filter genres by name (ex. ?name=Drama)",
            ),
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class PlayViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    filter_backends = (DjangoFilterBackend,)
    filterset_class = PlayFilterSet
    queryset = (
        Play
        .objects
        .prefetch_related(
            "genres",
            "actors",
            "performances__theatre_hall"
        )
    )
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly,)

    def get_serializer_class(self):
        if self.action == "retrieve":
            return PlayDetailSerializer
        if self.action == "list":
            return PlayListSerializer
        if self.action == "upload_image":
            return PlayImageSerializer
        return PlaySerializer

    @action(
        methods=["POST"],
        detail=True,
        url_path="upload-image",
    )
    def upload_image(self, request, pk=None):
        movie = self.get_object()
        serializer = self.get_serializer(movie, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        parameters=[
            OpenApiParameter(
                "title",
                type=OpenApiTypes.STR,
                description="Filter plays by title (ex. ?title=Hamlet)",
            ),
            OpenApiParameter(
                "genres",
                type={"type": "array", "items": {"type": "integer"}},
                description="Filter plays by "
                            "comma-separated genre ids "
                            "(ex. ?genres=1,2,3)",
            ),
            OpenApiParameter(
                "actors",
                type={"type": "array", "items": {"type": "integer"}},
                description="Filter plays by "
                            "comma-separated actor ids "
                            "(ex. ?actors=5,7)",
            ),
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class PerformanceViewSet(ModelViewSet):
    queryset = (
        Performance
        .objects
        .select_related("play", "theatre_hall")
        .prefetch_related("tickets", "play__actors", "play__genres")
        .annotate(
            tickets_available=(
                F("theatre_hall__rows") * F("theatre_hall__seats_in_row")
                - Count("tickets")
            )
        )
    )
    permission_classes = (IsAuthorizedOrIfAuthenticatedReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = PerformanceFilterSet

    def get_serializer_class(self):
        if self.action == "retrieve":
            return PerformanceDetailSerializer
        if self.action == "list":
            return PerformanceListSerializer
        return PerformanceSerializer

    @extend_schema(
        parameters=[
            OpenApiParameter(
                "play",
                type=OpenApiTypes.INT,
                description="Filter by play id (ex. ?play=2)",
            ),
            OpenApiParameter(
                "date",
                type=OpenApiTypes.DATE,
                description=(
                    "Filter by datetime of Performance "
                    "(ex. ?date=2022-10-23)"
                ),
            ),
            OpenApiParameter(
                "hall",
                type=OpenApiTypes.DATE,
                description=(
                    "Filter by theatre hall of Performance "
                    "(ex. ?hall=1)"
                ),
            ),
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class ReservationViewSet(ModelViewSet):
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly,)

    def get_queryset(self):
        if getattr(self, "swagger_fake_view", False):
            return Reservation.objects.none()

        return (
            Reservation
            .objects
            .filter(user=self.request.user)
            .prefetch_related(
                "tickets",
                "tickets__performance",
                "tickets__performance__play"
            ))

    def get_serializer_class(self):
        if self.action == "list":
            return ReservationListSerializer
        return ReservationSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)


class TheatreHallViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    GenericViewSet,
):
    queryset = TheatreHall.objects.all()
    serializer_class = TheatreHallSerializer
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly,)
