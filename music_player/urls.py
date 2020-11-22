from django.conf import settings
from django.urls import include, path
from django.conf.urls.static import static

from rest_framework_simplejwt.views import (
    TokenRefreshView,
    TokenVerifyView
)

from music_player.core.jwToken.jwtViewSet import UserTokenView


from api.urls import api_router


urlpatterns = [
    path('api/v1/token', UserTokenView.as_view()),
    path('api/v1/token/refresh', TokenRefreshView.as_view()),
    path('api/v1/token/verify', TokenVerifyView.as_view()),
    path('api/v1/', include(api_router.urls)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    try:
        import debug_toolbar
        urlpatterns.append(path('__debug__/', include(debug_toolbar.urls)))
    except ImportError:
        pass
