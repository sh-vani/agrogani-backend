# adminauth/auth.py

from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken
from .models import AdminUser

class AdminJWTAuthentication(JWTAuthentication):
    def get_user(self, validated_token):
        try:
            user_id = validated_token['user_id']
        except KeyError:
            raise InvalidToken('Token contained no recognizable user identification')

        try:
            user = AdminUser.objects.get(id=user_id, is_active=True)
        except AdminUser.DoesNotExist:
            raise InvalidToken('User not found')

        return user