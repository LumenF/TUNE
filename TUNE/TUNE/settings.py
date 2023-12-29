# using Django 4.1.7.
import ast
import os
from os.path import join, dirname

from pathlib import Path

import redis
from dotenv import load_dotenv, find_dotenv

from telebot import TeleBot

from celery.schedules import crontab

load_dotenv()
DEVELOPMENT = os.getenv('DEVELOPMENT', 'False').lower() == 'true'

if DEVELOPMENT:
    ENV = find_dotenv(filename='.dev.env')
    print('START DEVELOPMENT SCRIPT')
else:
    print('START PRODUCTION SCRIPT')
    ENV = find_dotenv(filename='.prod.env')

load_dotenv(ENV)

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv('SECRET_KEY')

DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'
DEVELOPMENT = os.getenv('DEVELOPMENT', 'False').lower() == 'true'

ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS').split(',')


INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rangefilter',
    'storages',

    'bootstrap5',
    'apps.apps.logs',
    'apps.abstraction',
    'apps.apps.user',
    'apps.apps.configs.geography',
    'apps.apps.configs.parameter',
    'apps.apps.configs.product_conf',
    'apps.apps.product',
    'apps.apps.mailing',
    'crispy_forms',
    'django_filters',

    'apps.site.index',
    'apps.site.site_product',

]

AUTH_USER_MODEL = 'user.UserModel'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # 'whitenoise.middleware.WhiteNoiseMiddleware',
]

ROOT_URLCONF = 'TUNE.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'apps/abstraction/templates')],
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

WSGI_APPLICATION = 'TUNE.wsgi.application'


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.environ.get('MYSQL_DATABASE'),
        'USER': os.environ.get('MYSQL_USER'),
        'PASSWORD': os.environ.get('MYSQL_PASSWORD'),
        'HOST': os.environ.get('MYSQL_DATABASE_HOST'),
        'PORT': os.environ.get('MYSQL_DATABASE_PORT'),
        'OPTIONS': {
                    'charset': 'utf8mb4',
                    'use_unicode': True,
                    'sql_mode': 'traditional',
        },
    }
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


# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'ru'

TIME_ZONE = 'Europe/Moscow'

USE_I18N = True
USE_L10N = True
USE_TZ = True

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

PROD_DOMAIN = os.environ.get('PROD_DOMAIN')
DEV_DOMAIN = os.environ.get('DEV_DOMAIN')
CSRF_TRUSTED_ORIGINS = [
    f'https://{PROD_DOMAIN}',
    f'https://www.{PROD_DOMAIN}',
    f'http://{DEV_DOMAIN}',
    f'http://www.{DEV_DOMAIN}',
    f'http://{PROD_DOMAIN}',
    f'http://www.{PROD_DOMAIN}',
    f'http://0.0.0.0:8002',
    f'http://web',
    f'http://localhost',
]
CORS_ALLOWED_ORIGINS = [
    f'https://{PROD_DOMAIN}',
    f'https://www.{PROD_DOMAIN}',
    f'http://{DEV_DOMAIN}',
    f'http://www.{DEV_DOMAIN}',
    f'http://{PROD_DOMAIN}',
    f'http://www.{PROD_DOMAIN}',
    f'http://0.0.0.0:8002',
    f'http://web',
    f'http://localhost',
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

DATA_UPLOAD_MAX_NUMBER_FIELDS = 10000
# CRISPY_TEMPLATE_PACK = 'bootstrap4'

########
# Redis settings
########
REDIS_PASSWORD = os.getenv('REDIS_PASSWORD')
REDIS_HOST = os.getenv('REDIS_HOST')
REDIS_PORT = os.getenv('REDIS_PORT')
REDIS_DB = os.getenv('REDIS_DB')

CELERY_BROKER_URL = f'redis://:{REDIS_PASSWORD}@{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB}'
CELERY_BROKER_TRANSPORT_OPTIONS = {'visibility_timeout': 1}
CELERY_RESULT_BACKEND = CELERY_BROKER_URL
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_ALWAYS_EAGER = False

s_redis_user = redis.Redis(
    host=os.getenv('REDIS_HOST'),
    port=os.getenv('REDIS_PORT'),
    password=os.getenv('REDIS_PASSWORD'),
    db=15
)

#########
# Статика и медиа

USE_S3 = ast.literal_eval(os.getenv('USE_S3'))

if USE_S3:
    # aws settings
    AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
    AWS_STORAGE_BUCKET_NAME = os.getenv('AWS_STORAGE_BUCKET_NAME')
    AWS_S3_ENDPOINT_URL = os.getenv('AWS_S3_ENDPOINT_URL')

    AWS_DEFAULT_ACL = 'public-read'

    AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.timeweb.com'
    AWS_S3_OBJECT_PARAMETERS = {
        'CacheControl': 'max-age=86400',
    }

    STATIC_LOCATION = 'tune/static'
    STATIC_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/{STATIC_LOCATION}/'
    STATICFILES_STORAGE = 'TUNE.storage.StaticStorage'

    PUBLIC_MEDIA_LOCATION = 'tune/media'
    MEDIA_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/{PUBLIC_MEDIA_LOCATION}/'
    DEFAULT_FILE_STORAGE = 'TUNE.storage.PublicMediaStorage'


else:
    MEDIA_URL = '/media/'
    MEDIA_ROOT = os.path.join(BASE_DIR, "media")

    STATIC_URL = '/static/'
    STATIC_ROOT = os.path.join(BASE_DIR, 'static')
    STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

    MIDDLEWARE.append('whitenoise.middleware.WhiteNoiseMiddleware')

AWS_PATH = os.getenv('AWS_PATH')

client = TeleBot(
    token=os.getenv('BOT_TOKEN'),
    parse_mode='HTML',
)

TUNE_BASE_URL='http://tuneapp.ru/'