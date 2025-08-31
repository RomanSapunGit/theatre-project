import datetime
import random

from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.utils import timezone
from user.utils import send_verification_email, generate_verification_code

from user.serializers import UserSerializer, EmailVerificationSerializer


# Create your views here.
class CreateUserView(generics.CreateAPIView):
    serializer_class = UserSerializer


class ManageUserView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    authentication_classes = (JWTAuthentication,)

    def get_object(self):
        return self.request.user


class VerifyUserEmailView(APIView):
    authentication_classes = (JWTAuthentication,)

    def get_object(self):
        return self.request.user

    def post(self, request, *args, **kwargs):
        user = self.get_object()

        if user.is_email_verified:
            return Response(
                {"detail": "Email is already verified."},
                status=status.HTTP_400_BAD_REQUEST
            )

        if user.verification_code_timeout and user.verification_code_timeout > timezone.now():
            return Response(
                {"error": "Email sending timeout is not over yet."},
                status=status.HTTP_400_BAD_REQUEST
            )

        verification_code = generate_verification_code()
        send_verification_email(user, verification_code)

        user.verification_code = verification_code
        user.verification_code_timeout = timezone.now() + datetime.timedelta(minutes=3)
        user.save()

        return Response(status=status.HTTP_204_NO_CONTENT)

    def put(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = EmailVerificationSerializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)

        user.is_email_verified = True
        user.verification_code = None
        user.verification_code_timeout = None
        user.save()

        return Response(status=status.HTTP_204_NO_CONTENT)
