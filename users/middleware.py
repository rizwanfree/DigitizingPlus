from django.utils.deprecation import MiddlewareMixin
from django.contrib.auth import get_user_model

from users.models import User

# users/middleware.py
class ImpersonateUserMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user_id = request.session.get('impersonate_id')
        if user_id:
            try:
                # Store the original user before impersonating
                request.original_user = request.user
                impersonated_user = User.objects.get(id=user_id)
                request.user = impersonated_user
                request.is_impersonating = True
            except User.DoesNotExist:
                request.is_impersonating = False
        else:
            request.is_impersonating = False

        response = self.get_response(request)
        return response
