from . import models
from django import forms
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserCreationForm
from .utils import get_albuns, get_generos, get_bandas


class UsuarioAdmin(UserAdmin):
    model = models.Usuario
    fieldsets = (
        (None,
         {
            'fields': ('email', 'nome', 'sobrenome', 'avatar', 'password')
         }),
    )
    list_display = ('email', 'nome', 'sobrenome', 'is_staff')
    list_filter = ('email', 'nome', 'sobrenome',)
    search_fields = ('email', 'nome', 'sobrenome',)
    ordering = ('email', 'nome',)
    filter_horizontal = ('groups', 'user_permissions',)


class UsuarioForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(
            attrs={'class': 'form-control', 'placeholder': 'Email'}
        )
    )
    nome = forms.CharField(
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'Nome'}
        )
    )
    sobrenome = forms.CharField(
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'Sobrenome'}
        )
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Senha'
            }
        )
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Confirme sua senha'
            }
        )
    )
    avatar = forms.FileField(
        required=False,
        widget=forms.FileInput(
            attrs={'placeholder': 'Avatar'}
        )
    )

    class Meta:
        model = models.Usuario
        fields = (
            'email', 'nome', 'sobrenome', 'password1', 'password2', 'avatar'
        )


class UsuarioEditAvatar(forms.ModelForm):
    avatar = forms.FileField(
        required=False,
        widget=forms.FileInput(
            attrs={'placeholder': 'Avatar'}
        )
    )

    class Meta:
        model = models.Usuario
        fields = ('avatar',)


class GeneroForm(forms.ModelForm):
    descricao = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control', 'placeholder': 'Descrição'
            }
        )
    )
    imagen = forms.ImageField(
        widget=forms.FileInput(
            attrs={
                'class': 'form-control-file', 'placeholder': 'Imagen'
            }
        )
    )

    class Meta:
        fields = ('descricao', 'imagen',)
        model = models.Genero


class BandaForm(forms.ModelForm):
    nome = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control', 'placeholder': 'Nome'
            }
        )
    )

    genero = forms.ModelChoiceField(
        queryset=get_generos(),
        widget=forms.Select(
            attrs={
                'class': 'form-control selectpicker', 'placeholder': 'Genero',
                'data-live-search': 'true', 'data-style': 'btn-primary',
                'title': 'Escolha um genero'
            })
    )

    imagem = forms.ImageField(
        widget=forms.FileInput(
            attrs={
                'class': 'form-control-file', 'placeholder': 'Imagem'
            }
        )
    )

    class Meta:
        fields = ('nome', 'genero', 'imagem',)
        model = models.Banda


class AlbumForm(forms.ModelForm):
    nome = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control', 'placeholder': 'Nome'
            }
        )
    )

    banda = forms.ModelChoiceField(
        queryset=get_bandas(),
        widget=forms.Select(
            attrs={
                'class': 'form-control selectpicker', 'placeholder': 'Banda',
                'data-live-search': 'true', 'data-style': 'btn-primary',
                'title': 'Escolha uma banda'
            })
    )

    data_lancamento = forms.IntegerField(
        widget=forms.NumberInput(
            attrs={
                'class': 'form-control', 'placeholder': 'Data de lançamento'
            }
        )
    )

    capa = forms.ImageField(
        widget=forms.FileInput(
            attrs={
                'class': 'form-control-file', 'placeholder': 'Capa'
            }
        )
    )

    class Meta:
        fields = ('nome', 'banda', 'data_lancamento', 'capa',)
        model = models.Album


class MusicaForm(forms.ModelForm):
    nome = forms.CharField(
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'Nome'}
        )
    )

    album = forms.ModelChoiceField(
        queryset=get_albuns(),
        widget=forms.Select(
            attrs={
                'class': 'form-control selectpicker', 'placeholder': 'Album',
                'data-live-search': 'true', 'data-style': 'btn-primary',
                'title': 'Escolha um album'
            })
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
        exclude = ('arquivo_tipo', 'duracao',)
