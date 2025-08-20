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


class TheatreHallSerializer(serializers.ModelSerializer):
    class Meta:
        model = TheatreHall
        fields = ("id", "name", "rows", "seats_in_row")


class PerformanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Performance
        fields = ("id", "play", "theatre_hall", "show_time")


class PerformanceDetailSerializer(PerformanceSerializer):
    theater_hall = TheatreHallSerializer(many=True, read_only=True)


class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = ("id", "created_at", "user")


class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ("id", "row", "seat", "performance", "reservation")


class TicketDetailSerializer(TicketSerializer):
    performance = PerformanceDetailSerializer(read_only=True)
