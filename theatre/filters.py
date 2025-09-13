from django_filters import (
    rest_framework as
    filters,
    BaseInFilter,
    NumberFilter
)


class NumberInFilter(BaseInFilter, NumberFilter):
    pass


class PlayFilterSet(filters.FilterSet):
    title = filters.CharFilter(field_name="title", lookup_expr="icontains")
    genres = NumberInFilter(field_name="genres__id", lookup_expr="in")
    actors = NumberInFilter(field_name="actors__id", lookup_expr="in")


class PerformanceFilterSet(filters.FilterSet):
    date = filters.DateFilter(field_name="show_time__date")
    play = filters.NumberFilter(field_name="play__id")
    hall = filters.NumberFilter(field_name="theatre_hall__id")

    @property
    def qs(self):
        parent = super().qs
        user = getattr(self.request, "user", None)

        if user and user.theatre_hall:
            parent = parent.filter(theatre_hall=user.theatre_hall)
        return parent


class GenreFilterSet(filters.FilterSet):
    name = filters.CharFilter(field_name="name", lookup_expr="icontains")


class ActorFilterSet(filters.FilterSet):
    first_name = filters.CharFilter(
        field_name="first_name",
        lookup_expr="icontains"
    )
    last_name = filters.CharFilter(
        field_name="last_name",
        lookup_expr="icontains"
    )
