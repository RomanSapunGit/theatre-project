from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)

from user.views import (
    CreateUserView,
    ManageUserView,
    VerifyUserEmailView
)

urlpatterns = [
    path("register/", CreateUserView.as_view(), name="create"),
    path("tokens/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("tokens/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("tokens/verify/", TokenVerifyView.as_view(), name="token_verify"),
    path("me/", ManageUserView.as_view(), name="manage"),
    path("verify-email/", VerifyUserEmailView.as_view(), name="email_verify")
]

app_name = "user"
