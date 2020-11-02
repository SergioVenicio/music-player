from django import forms

from .models import Music
from album.models import Album


class MusicForm(forms.ModelForm):
    name = forms.CharField(
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'Name'}
        )
    )

    album = forms.ModelChoiceField(
        queryset=Album.objects.all(),
        widget=forms.Select(
            attrs={
                'class': 'form-control selectpicker', 'placeholder': 'Album',
                'data-live-search': 'true', 'data-style': 'btn-primary',
                'title': 'Choice a album'
            })
    )

    order = forms.IntegerField(
        widget=forms.NumberInput(
            attrs={'class': 'form-control', 'placeholder': 'Order'}
        )
    )

    file = forms.FileField(
        widget=forms.FileInput(
            attrs={
                'class': 'form-control-file', 'placeholder': 'Music File'
            }
        )
    )

    class Meta:
        model = Music
        exclude = ('file_type', 'duration',)
