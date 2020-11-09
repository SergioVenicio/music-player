from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from django.conf.urls.static import static


from api.urls import api_router


urlpatterns = [
    path('api/v1/', include(api_router.urls)),
    path('', include('music_player.core.urls')),
    path('admin/', admin.site.urls),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    try:
        import debug_toolbar
        urlpatterns.append(path('__debug__/', include(debug_toolbar.urls)))
    except ImportError:
        pass
