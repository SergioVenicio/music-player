from rest_framework import serializers

from ..models import Band, Genre


class GenreSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    genre_image = serializers.SerializerMethodField()

    def get_genre_image(self, genre):
        image_path = genre.genre_image.url
        return f'http://localhost:8000{image_path}'

    class Meta:
        model = Genre
        fields = (
            'id',
            'description',
            'genre_image'
        )


class BandSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.ReadOnlyField()
    genre = serializers.ReadOnlyField(source='genre.description')

    class Meta:
        model = Band
        fields = ('__all__')
