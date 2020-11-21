from rest_framework import serializers

from ..models import Music


class BaseMusicSerializer(serializers.HyperlinkedModelSerializer):
    def get_file(self, music):
        context = self.context.get('request')
        file_path = music['file']
        return context.build_absolute_uri(file_path)


class MusicSerializer(BaseMusicSerializer):
    album = serializers.ReadOnlyField(source='album.name')
    file = serializers.SerializerMethodField()

    class Meta:
        model = Music
        fields = (
            'id',
            'name',
            'album',
            'order',
            'file',
        )


class MusicSerializerList(BaseMusicSerializer):
    album = serializers.ReadOnlyField(source='album.name')
    file = serializers.CharField()
    duration = serializers.CharField()

    class Meta:
        model = Music
        fields = (
            'id',
            'name',
            'album',
            'order',
            'file',
            'file_type',
            'duration'
        )
