from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsAdminOrIfAuthenticatedReadOnly(BasePermission):
    def _is_read_only_allowed(self, request):
        return (
            request.method in SAFE_METHODS
            and request.user
            and request.user.is_authenticated
        )

    def _is_admin(self, request):
        return request.user and request.user.is_staff

    def has_permission(self, request, view):
        return (
            request.user.is_email_verified
            and (self._is_read_only_allowed(request)
                 or self._is_admin(request))
        )


class IsAuthorizedOrIfAuthenticatedReadOnly(IsAdminOrIfAuthenticatedReadOnly):
    def has_permission(self, request, view):
        return (
            request.user.is_email_verified
            and (self._is_read_only_allowed(request)
                 or self._is_admin(request)
                 or (
                request.user
                and request.user.is_authenticated
                and request.user.is_hall_overseer
            )
            )
        )
