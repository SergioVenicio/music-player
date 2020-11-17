from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class UserTokenSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token['user'] = {
            'name': user.name,
            'last_name': user.last_name,
            'avatar': f'/media/{user.avatar}'
        }

        return token
