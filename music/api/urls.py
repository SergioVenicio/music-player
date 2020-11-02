from rest_framework.routers import SimpleRouter

from .viewset import MusicViewSet

music_router = SimpleRouter(trailing_slash=False)

music_router.register('music', viewset=MusicViewSet)
