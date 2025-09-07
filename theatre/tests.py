import requests
from django.contrib.auth import get_user_model
from django.db import connection
from django.test.utils import CaptureQueriesContext
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APIClient

from theatre.models import Reservation, Ticket, Performance, TheatreHall


def create_user_reservation(
        user,
        seat,
        row,
        performance_pk,
):
    reservation = Reservation.objects.create(
        created_at=timezone.now(),
        user=user
    )
    Ticket.objects.create(
        reservation=reservation,
        row=row,
        seat=seat,
        performance=Performance.objects.get(pk=performance_pk)
    )


def assign_theatre_hall(user):
    hall = TheatreHall.objects.get(pk=1)
    user.theatre_hall = hall
    user.save()

class BaseAuthorizedAPITest(TestCase):
    fixtures = ["theatre_data.json"]

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "test@test.com", "testpass"
        )
        self.user.is_email_verified = True
        self.user.is_staff = True
        self.user.save()
        self.client.force_authenticate(self.user)

    def get_theatre_url(self, theatre_path, **kwargs):
        return reverse(f"theatre:{theatre_path}", kwargs=kwargs)


class PlayViewTests(BaseAuthorizedAPITest):

    def test_play_detail_returns_nested_genres(self):
        response = self.client.get(self.get_theatre_url("play-detail", pk=1))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        expected_result = {"id": 1, "name": "Drama"}
        self.assertEqual(
            expected_result,
            response.data["genres"][0],
            "Genres field is not using nested serializers!"
        )

    def test_play_list_returns_slug_genres(self):
        response = self.client.get(self.get_theatre_url("play-list"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertTrue(
            isinstance(response.data[0]["genres"][0], str),
            "Genres are not a slug field!"
        )

    def test_play_upload_image(self):
        url = ("https://cdn.pixabay.com/photo/"
               "2023/11/16/05/02/mountains-8391433_640.jpg")
        image_response = requests.get(url)

        if image_response.status_code != 200:
            self.fail("Image is not available, please change image")
        image = SimpleUploadedFile(
            "test.jpeg",
            image_response.content,
            content_type="image/jpeg",
        )
        response = self.client.post(
            self.get_theatre_url("play-upload-image", pk=1),
            {"image": image},
            format="multipart",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

class ReservationViewTests(BaseAuthorizedAPITest):
    def test_no_duplicate_queries_in_reservation_viewset(self):
        create_user_reservation(self.user, 3, 3, 1)
        first_result = []
        with CaptureQueriesContext(connection) as ctx:
            response = self.client.get(
                self.get_theatre_url("reservation-list")
            )

            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertNotEqual(response.data, [])
            first_result = ctx.captured_queries

        create_user_reservation(self.user, 3, 4, 2)

        with CaptureQueriesContext(connection) as ctx2:
            response = self.client.get(
                self.get_theatre_url("reservation-list")
            )
            self.assertNotEqual(response.data, [])
            self.assertEqual(len(first_result), len(ctx2.captured_queries))

            sqls = [q["sql"] for q in ctx2.captured_queries]
            self.assertEqual(len(sqls), len(set(sqls)))

class PerformanceViewTests(BaseAuthorizedAPITest):
    def test_performance_filter_for_overseer_shows_only_by_theatre_hall(self):
        assign_theatre_hall(self.user)
        response = self.client.get(
            self.get_theatre_url("performance-list")
        )
        self.assertEqual(len(response.data), 1)

    def test_create_performance_by_overseer(self):
        assign_theatre_hall(self.user)
        response = self.client.post(
            self.get_theatre_url("performance-list"),
            data={
                "play": 1,
                "theatre_hall": 2,
                "show_time": timezone.now()
            }
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        response = self.client.post(
            self.get_theatre_url("performance-list"),
            data={
                "play": 1,
                "theatre_hall": 1,
                "show_time": timezone.now()
            }
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
