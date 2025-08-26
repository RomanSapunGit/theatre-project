from django.urls import path, include
from rest_framework import routers

from theatre.views import (
    ActorViewSet,
    GenreViewSet,
    PlayViewSet,
    PerformanceViewSet,
    ReservationViewSet,
    TheatreHallViewSet
)

router = routers.DefaultRouter()
router.register("actors", ActorViewSet)
router.register("genres", GenreViewSet)
router.register("plays", PlayViewSet)
router.register("reservations", ReservationViewSet, basename="Reservation")
router.register("performances", PerformanceViewSet)
router.register("theatre_halls", TheatreHallViewSet)

urlpatterns = [
    path("", include(router.urls))
]

app_name = "theatre"
