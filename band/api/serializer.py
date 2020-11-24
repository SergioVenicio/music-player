from rest_framework import serializers

from ..models import Band, Genre


class GenreSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    genre_image = serializers.SerializerMethodField()

    def get_genre_image(self, genre):
        image_path = genre['genre_image']
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
    band_image = serializers.SerializerMethodField()

    def get_band_image(self, band):
        image_path = band.get('band_image')

        print(band)

        if image_path is None:
            return ''

        return f'http://localhost:8000{image_path}'

    class Meta:
        model = Band
        fields = (
            'id',
            'name',
            'genre',
            'band_image'
        )
