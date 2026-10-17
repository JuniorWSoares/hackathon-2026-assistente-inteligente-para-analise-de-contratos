from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from core.modules.auth.service import display_name


class LoginSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token["name"] = display_name(user)
        token["role"] = user.role
        return token