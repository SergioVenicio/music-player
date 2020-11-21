from rest_framework import serializers


from ..models import User, Like


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = (
            'id',
            'email',
            'name',
            'last_name',
            'avatar'
        )


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        depth = 1
        model = Like
        fields = (
            'id',
            'user_id',
            'music_id'
        )
