from . import views
from django.urls import path
from django.contrib.auth import views as auth_views


USER_URLS = [
    path('login', auth_views.login, name='login'),
    path('sign_up', views.sign_up, name='sign_up'),
    path(
        'logout',
        auth_views.LogoutView.as_view(
            template_name='registration/logout.html'
        ),
        name='logout'
    ),
    path('avatar/', views.user_avatar, name='avatar'),
]

urlpatterns = [
    path('', views.home, name='home'),
    path('musicas/add', views.add_musicas, name="add_musicas"),
    path('musicas/<int:id>', views.musicas, name="musicas"),
    path('bandas/add', views.add_bandas, name="add_bandas"),
    path('bandas/<int:id>', views.bandas, name="bandas"),
    path('albuns/<int:id>', views.albuns, name="albuns"),
    path('albuns/add', views.add_albuns, name="add_albuns"),
    path('generos/add', views.add_generos, name="add_generos"),
] + USER_URLS
