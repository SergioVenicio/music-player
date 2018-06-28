release: python manage.py makemigrations
release: python manage.py migrate --noinput
web: gunicorn music_player.wsgi --log-file -
