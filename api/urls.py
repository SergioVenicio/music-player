from rest_framework.routers import DefaultRouter

from album.api.urls import album_router
from band.api.urls import band_router
from music.api.urls import music_router
from user.api.urls import user_router


api_router = DefaultRouter(trailing_slash=False)
api_router.registry.extend(album_router.registry)
api_router.registry.extend(band_router.registry)
api_router.registry.extend(music_router.registry)
api_router.registry.extend(user_router.registry)
