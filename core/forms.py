from . import models
from django import forms
from .utils import get_albuns


class MusicaForm(forms.ModelForm):
    nome = forms.CharField(
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'Nome'}
        )
    )

    album = forms.ModelChoiceField(
        queryset=get_albuns(),
        widget=forms.Select(
            attrs={'class': 'form-control', 'placeholder': 'Album'}
        )
    )

    ordem = forms.IntegerField(
        widget=forms.NumberInput(
            attrs={'class': 'form-control', 'placeholder': 'Ordem'}
        )
    )

    arquivo = forms.FileField(
        widget=forms.FileInput(
            attrs={
                'class': 'form-control-file', 'placeholder': 'Arquivo'
            }
        )
    )

    class Meta:
        model = models.Musica
        exclude = ('arquivo_tipo',)
