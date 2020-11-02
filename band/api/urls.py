from rest_framework.routers import SimpleRouter

from .viewset import BandViewSet, GenreViewSet

band_router = SimpleRouter(trailing_slash=False)

band_router.register('band', viewset=BandViewSet)
band_router.register('genre', viewset=GenreViewSet)
