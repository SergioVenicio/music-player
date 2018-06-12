from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from music_player.api.urls import router
from django.conf.urls.static import static


urlpatterns = [
    path('', include('music_player.core.urls')),
    path('admin/', admin.site.urls),
    path('api/v1/', include(router.urls)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
