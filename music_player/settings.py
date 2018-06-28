import os
from decouple import config
from dj_database_url import parse
from django.utils.crypto import get_random_string


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY = config('SECRET_KEY', get_random_string(50))

DEBUG = config('DEBUG', default=True, cast=bool)

ALLOWED_HOSTS = config('ALLOWED_HOSTS', ['*'])
AUTH_USER_MODEL = 'core.Usuario'

LOGIN_REDIRECT_URL = 'home'

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'music_player.core',
    'music_player.api',
    'rest_framework',
    'rest_framework.authtoken',
    'rest_auth',
    'corsheaders',
    'collectfast',
]


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',
]

ROOT_URLCONF = 'music_player.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'music_player.wsgi.application'

default_db_url = 'sqlite:///' + os.path.join(BASE_DIR, 'db.sqlite3')

DATABASES = {
    'default': config('DATABASE_URL', default=default_db_url, cast=parse)
}


REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    )
}


AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

LANGUAGE_CODE = 'pt-br'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


STATIC_URL = '/static/'

COLLECTFAST_ENABLED = False

AWS_ACCESS_KEY_ID = config('AWS_ACCESS_KEY_ID', None)
if AWS_ACCESS_KEY_ID is not None:
    COLLECTFAST_ENABLED = True
    INSTALLED_APPS.append('s3_folder_storage')
    INSTALLED_APPS.append('storages')
    AWS_SECRET_ACCESS_KEY = config('AWS_SECRET_ACCESS_KEY')
    AWS_STORAGE_BUCKET_NAME = config('AWS_STORAGE_BUCKET_NAME')
    AWS_S3_OBJECT_PARAMETERS = {'CacheControl': 'max-age=86400', }
    AWS_PRELOAD_METADATA = True
    AWS_AUTO_CREATE_BUCKET = False
    AWS_QUERYSTRING_AUTH = False
    AWS_EXPIRY = 60 * 60 * 24 * 7

    control = f'''
        max-age={AWS_EXPIRY:d}, s-maxage={AWS_EXPIRY:d}, must-revalidate
    '''

    DEFAULT_FILE_STORAGE = 's3_folder_storage.s3.DefaultStorage'
    DEFAULT_S3_PATH = 'media'
    MEDIA_ROOT = f'//{DEFAULT_S3_PATH}'
    MEDIA_URL = f'//s3.amazonaws.com/{AWS_STORAGE_BUCKET_NAME}/{DEFAULT_S3_PATH}/'

    STATICFILES_STORAGE = 's3_folder_storage.s3.StaticStorage'
    STATIC_S3_PATH = 'static'
    STATIC_ROOT = f'//{STATIC_S3_PATH}'
    STATIC_URL = f'//s3.amazonaws.com/{AWS_STORAGE_BUCKET_NAME}/{STATIC_S3_PATH}/'
    ADMIN_MEDIA_PREFIX = STATIC_URL + 'admin/'
else:
    MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
    MEDIA_URL = '/media/'
    STATIC_URL = '/static/'

    if DEBUG:
        STATICFILES_DIRS = [
            os.path.join(BASE_DIR, 'static'),
        ]
    else:
        STATIC_ROOT = os.path.join(BASE_DIR, 'static')

# Corsheaders
CORS_ORIGIN_ALLOW_ALL = True

PERPAGE = 15
