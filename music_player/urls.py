from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from django.conf.urls.static import static


urlpatterns = [
    path('api/v1/', include('music_player.api.urls')),
    path('', include('music_player.core.urls')),
    path('admin/', admin.site.urls),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
