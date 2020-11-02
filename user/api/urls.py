from rest_framework.routers import SimpleRouter

from .viewset import LikesViewSet, UserViewSet

user_router = SimpleRouter(trailing_slash=False)

user_router.register('user', viewset=UserViewSet)
user_router.register('likes', viewset=LikesViewSet)
