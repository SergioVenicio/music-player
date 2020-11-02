from rest_framework.routers import SimpleRouter

from .viewset import AlbumViewSet

album_router = SimpleRouter(trailing_slash=False)

album_router.register('album', viewset=AlbumViewSet)
