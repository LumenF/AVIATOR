# using Django 4.1.4
import ast
import os
from pathlib import Path

import redis

BASE_DIR = Path(__file__).resolve().parent.parent

DJANGO_ALLOW_ASYNC_UNSAFE = True

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'admin_extra_buttons',
    'ninja_extra',
    'drf_yasg',
    'utils',
    'user',
    'mailing',
    'channel',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
]

ROOT_URLCONF = 'AVIATOR.urls'

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

WSGI_APPLICATION = 'AVIATOR.wsgi.application'

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

LANGUAGE_CODE = 'ru'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

########
# .env data
########

DEVELOPMENT = ast.literal_eval(os.getenv('DEVELOPMENT'))
DEBUG = ast.literal_eval(os.getenv('DEBUG'))
MEDIA_PATH = 'C:\\Users\\lindel\\Desktop\\AVIATIOR\\aviator\\'
if DEBUG:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': os.environ.get('MYSQL_DATABASE'),
            'USER': os.environ.get('DEV_MYSQL_USER') if DEVELOPMENT else os.environ.get('MYSQL_USER'),
            'PASSWORD': os.environ.get('DEV_MYSQL_PASSWORD')if DEVELOPMENT else os.environ.get('MYSQL_PASSWORD'),
            'HOST': os.environ.get('DEV_MYSQL_DATABASE_HOST') if DEVELOPMENT else os.environ.get('MYSQL_DATABASE_HOST'),
            'PORT': os.environ.get('MYSQL_DATABASE_PORT'),
            'OPTIONS': {
                        'charset': 'utf8mb4',
                        'use_unicode': True,
            },
        }
    }
SECRET_KEY = os.getenv('SECRET_KEY')

ALLOWED_HOSTS = ast.literal_eval(os.environ.get('ALLOWED_HOSTS'))

########
# HTTPS\CSRF
########
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

CSRF_TRUSTED_ORIGINS = [
    'https://j4exchange.tk',
    'https://www.j4exchange.tk',
]
CORS_ALLOWED_ORIGINS = [
    'https://j4exchange.tk',
    'https://www.j4exchange.tk',
]
CORS_ALLOW_ALL_ORIGINS = True

CORS_ALLOW_METHODS = [
    "DELETE",
    "GET",
    "OPTIONS",
    "PATCH",
    "POST",
    "PUT",
]
CORS_ALLOW_HEADERS = [
    "accept",
    "accept-encoding",
    "authorization",
    "content-type",
    "dnt",
    "origin",
    "user-agent",
    "x-csrftoken",
    "x-requested-with",
]

########
# Redis settings
########
REDIS_HOST = os.getenv('DEV_REDIS_HOST') if DEVELOPMENT else os.getenv('REDIS_HOST')
REDIS_PORT = os.getenv('DEV_REDIS_PORT') if DEVELOPMENT else os.getenv('REDIS_PORT')
CELERY_BROKER_URL = 'redis://' + REDIS_HOST + ':' + REDIS_PORT + '/0'
CELERY_BROKER_TRANSPORT_OPTIONS = {'visibility_timeout': 1}
CELERY_RESULT_BACKEND = 'redis://' + REDIS_HOST + ':' + REDIS_PORT + '/0'
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_ALWAYS_EAGER = False
s_redis_user = redis.Redis(host=REDIS_HOST,
                           port=int(REDIS_PORT),
                           db=int(os.getenv('REDIS_TELEGRAM_USER')),
                           )
