from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from django.conf.urls.static import static
from music_player.core import views, viewset
from rest_framework.routers import DefaultRouter
from django.contrib.auth import views as auth_views

router = DefaultRouter(trailing_slash=False)
router.register(r'genero', viewset.GeneroViewSet, base_name='genero')
router.register(r'banda', viewset.BandaViewSet, base_name='banda')
router.register(r'album', viewset.AlbumViewSet, base_name='album')
router.register(r'musicas', viewset.MusicaViewSet, base_name='musica')
router.register(
    r'musicas/album/(?P<album_id>.+)', viewset.MusicaViewSet,
    base_name='musica_filter'
)

app_name = "music-player"
USER_URLS = [
    path('login', auth_views.login, name='login'),
    path('sign_up', views.sign_up, name='sign_up'),
    path(
        'logout',
        auth_views.LogoutView.as_view(
            template_name='registration/logout.html'
        ),
        name='logout'
    ),
]
urlpatterns = [
    path('', views.home, name='home'),
    path('musicas/<int:album_id>/', views.musicas, name="musicas"),
    path('musicas/add/', views.add_musicas, name="add_musicas"),
    path('bandas/<int:genero_id>/', views.bandas, name="bandas"),
    path('albuns/<int:banda_id>/', views.albuns, name="albuns"),
    path('generos/add', views.add_generos, name="add_generos"),
    path('admin/', admin.site.urls),
    path('api_v1/', include(router.urls)),
] + USER_URLS + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
