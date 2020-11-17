from rest_framework_simplejwt.views import TokenObtainPairView

from .jwtSerializer import UserTokenSerializer


class UserTokenView(TokenObtainPairView):
    serializer_class = UserTokenSerializer
