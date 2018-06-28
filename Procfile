release: python manage.py makemigrations core
release: python manage.py migrate --noinput
web: gunicorn music_player.wsgi --log-file -
