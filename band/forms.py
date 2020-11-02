from django import forms

from .models import Band, Genre


class GernreForm(forms.ModelForm):
    description = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control', 'placeholder': 'Description'
            }
        )
    )

    genre_image = forms.ImageField(
        widget=forms.FileInput(
            attrs={
                'class': 'form-control-file', 'placeholder': 'Genre image'
            }
        )
    )

    class Meta:
        fields = ('description', 'genre_image',)
        model = Genre


class BandForm(forms.ModelForm):
    name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control', 'placeholder': 'Name'
            }
        )
    )

    genre = forms.ModelChoiceField(
        queryset=Genre.objects.all(),
        widget=forms.Select(
            attrs={
                'class': 'form-control selectpicker', 'placeholder': 'Genre',
                'data-live-search': 'true', 'data-style': 'btn-primary',
                'title': 'Choice a musical genre'
            })
    )

    band_image = forms.ImageField(
        widget=forms.FileInput(
            attrs={
                'class': 'form-control-file', 'placeholder': 'Band image'
            }
        )
    )

    class Meta:
        fields = ('name', 'genre', 'band_image',)
        model = Band
