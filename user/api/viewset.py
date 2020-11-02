import json

from rest_framework import viewsets
from rest_framework.response import Response

from ..models import User, Like
from .serializer import LikeSerializer, UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    http_method_names = ['get']


class LikesViewSet(viewsets.ModelViewSet):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    http_method_names = ['get', 'post', 'delete', 'head']

    def get_queryset(self):
        queryset = Like.objects.all()
        user_id = self.request.query_params.get('user_id')
        music_id = self.request.query_params.get('music_id')

        if user_id is not None:
            queryset = queryset.filter(user_id=user_id)

        if music_id is not None:
            queryset = queryset.filter(music_id=music_id)

        return queryset

    def create(self, request, *args, **kwargs):
        user_id = request.data.get('user_id', None)
        music_id = request.data.get('music_id', None)

        if user_id is None:
            return Response(
                data={
                    'status': 'error',
                    'error': 'user_id field is required!'
                },
                status=403
            )
        if music_id is None:
            return Response(
                data={
                    'status': 'error',
                    'error': 'music_id field is required!'
                },
                status=403
            )

        like = Like.objects.filter(
            user_id=user_id,
            music_id=music_id
        ).first()

        if not like:
            like = Like(
                user_id=user_id,
                music_id=music_id
            )
            like.save()

        response = json.dumps({
            'like': {
                'id': like.id,
                'user_id': like.user.id,
                'music_id': like.music.id,
                'date': str(like.date)
            }
        })

        return Response(response, status=201)
