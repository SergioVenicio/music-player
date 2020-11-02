from rest_framework import serializers


from ..models import Album


class AlbumSerializer(serializers.HyperlinkedModelSerializer):
    band = serializers.ReadOnlyField(source='band.name')

    class Meta:
        model = Album
        fields = ('__all__')
