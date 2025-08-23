from django.db import transaction
from rest_framework import serializers

from theater.models import Actor, Genre, Play, Performance, TheatreHall, Ticket, Reservation


class ActorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Actor
        fields = ("id", "first_name", "last_name")


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ("id", "name")


class PlaySerializer(serializers.ModelSerializer):
    class Meta:
        model = Play
        fields = (
            "id",
            "title",
            "description",
            "actors",
            "genres"
        )


class PlayDetailSerializer(PlaySerializer):
    genres = GenreSerializer(
        read_only=True,
        many=True
    )
    actors = ActorSerializer(
        read_only=True,
        many=True
    )

    class Meta:
        model = Play
        fields = PlaySerializer.Meta.fields


class PlayListSerializer(PlaySerializer):
    genres = serializers.SlugRelatedField(
        read_only=True,
        many=True,
        source="name"
    )
    actors = serializers.SlugRelatedField(
        read_only=True,
        many=True,
        source="full_name"
    )
    tickets_available = serializers.IntegerField(
        read_only=True
    )

    class Meta:
        model = Play
        fields = PlaySerializer.Meta.fields + ("tickets_available",)


class TheatreHallSerializer(serializers.ModelSerializer):
    class Meta:
        model = TheatreHall
        fields = ("id", "name", "rows", "seats_in_row")


class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ("id", "row", "seat", "performance", "reservation")


class TicketSeatsSerializer(TicketSerializer):
    class Meta:
        model = Ticket
        fields = ("row", "seat")


class PerformanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Performance
        fields = ("id", "play", "theatre_hall", "show_time")


class PerformanceDetailSerializer(PerformanceSerializer):
    play = PlayDetailSerializer(read_only=True)
    taken_places = TicketSeatsSerializer(
        source="tickets",
        many=True,
        read_only=True
    )

    class Meta:
        model = Performance
        fields = ("id", "play", "theatre_hall", "show_time", "taken_places")


class PerformanceListSerializer(PerformanceSerializer):
    theatre_hall_name = serializers.CharField(
        source="theatre_hall.name", read_only=True
    )
    theatre_hall_capacity = serializers.CharField(
        source="theatre_hall.capacity", read_only=True
    )
    tickets_available = serializers.IntegerField(
        read_only=True
    )

    class Meta:
        model = Performance
        fields = (
            "id",
            "theatre_hall_name",
            "theatre_hall_capacity",
            "show_time",
            "tickets_available",
        )


class TicketListSerializer(TicketSerializer):
    performance = PerformanceListSerializer(
        many=False, read_only=True
    )
    play_name = serializers.CharField(
        read_only=True,
        source="performance.play"
    )
    class Meta:
        model = Ticket
        fields = TicketSerializer.Meta.fields + ("play_name",)


class PlayListSerializer(PlaySerializer):
    genres = serializers.SlugRelatedField(
        read_only=True,
        many=True,
        slug_field="name"
    )
    actors = serializers.SlugRelatedField(
        read_only=True,
        many=True,
        slug_field="full_name"
    )
    performances = PerformanceListSerializer(
        many=True,
        read_only=True
    )

    class Meta:
        model = Play
        fields = PlaySerializer.Meta.fields + ("performances",)


class ReservationSerializer(serializers.ModelSerializer):
    tickets = TicketSerializer(many=True, read_only=False, allow_empty=False)

    class Meta:
        model = Reservation
        fields = ("id", "created_at", "user")

    def create(self, validated_data):
        with transaction.atomic():
            tickets_data = validated_data.pop("tickets")
            reservation = Reservation.objects.create(**validated_data)
            for ticket_data in tickets_data:
                Ticket.objects.create(reservation=reservation, **ticket_data)
            return reservation


class TicketDetailSerializer(TicketSerializer):
    performance = PerformanceDetailSerializer(read_only=True)



class PlayImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Play
        fields = ("id", "image")
