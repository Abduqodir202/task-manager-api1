from rest_framework.throttling import UserRateThrottle


class PostRateThrottle(UserRateThrottle):
    scope = "post"

    def allow_request(self, request, view):
        if request.method == "POST":
            return super().allow_request(request, view)
        return True