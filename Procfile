release: python manage.py makemigrations core
release: python manage.py migrate
web: gunicorn music_player.wsgi --log-file -
