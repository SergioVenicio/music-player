from django import forms

from .models import Album
from band.models import Band


class AlbumForm(forms.ModelForm):
    name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control', 'placeholder': 'Name'
            }
        )
    )

    band = forms.ModelChoiceField(
        queryset=Band.objects.all(),
        widget=forms.Select(
            attrs={
                'class': 'form-control selectpicker', 'placeholder': 'Band',
                'data-live-search': 'true', 'data-style': 'btn-primary',
                'title': 'Choice a band'
            })
    )

    release_date = forms.IntegerField(
        widget=forms.NumberInput(
            attrs={
                'class': 'form-control', 'placeholder': 'Release date'
            }
        )
    )

    cover_image = forms.ImageField(
        widget=forms.FileInput(
            attrs={
                'class': 'form-control-file', 'placeholder': 'Cover image'
            }
        )
    )

    class Meta:
        fields = ('name', 'band', 'release_date', 'cover_image',)
        model = Album
