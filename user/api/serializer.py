from django.contrib.auth import get_user_model
from rest_framework import serializers


from ..models import User, Like


class UserSerializer(serializers.HyperlinkedModelSerializer):
    password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        UserModel = get_user_model()
        user = UserModel.objects.create_user(**validated_data)
        return user

    class Meta:
        model = User

        fields = (
            'id',
            'email',
            'name',
            'last_name',
            'avatar',
            'password'
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
