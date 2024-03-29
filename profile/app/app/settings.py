"""
Django settings for app project.

Generated by 'django-admin startproject' using Django 4.2.6.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

from pathlib import Path
import os
import logging

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

CSRF_TRUSTED_ORIGINS = ['https://bmini.ru']
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-q7+s2k(oj5w2a(2d-4(2s^9-^1y2to_v(ir^zr+2&gphw3sa41'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*', 'localhost']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'user_profile',
    'profile',
    'flags',
    'rest_framework',
    'django_filters',
    'django.contrib.postgres',
#    'createsuperuserifnotexists',

]

FLAGS = {
'FLAG_WITH_EMPTY_CONDITIONS': [],
'SEARCHS_FLAG': [],
'USERS_CREATE_FLAG': [],
'USERS_UPDATE_FLAG': [],
'USERS_DESTROY_FLAG': [],
'USERSDETAIL_FLAG': [],
}

REST_FRAMEWORK = {
    'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend']
}

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'app.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'app.wsgi.application'


# DATABASES = {
#     'default': {
#         #'ENGINE': os.getenv('DB_ENGINE', 'django.db.backends.postgresql'),  'django.db.backends.postgresql_psycopg2'
#         'ENGINE': os.getenv('DB_ENGINE', 'django.db.backends.postgresql_psycopg2'),
#         'NAME': os.getenv('DB_NAME', 'postgres'),
#         'USER': os.getenv('DB_USER', 'postgres'),
#         'PASSWORD': os.getenv('DB_USER_PASSWORD', 'postgres'),
#         'HOST': os.getenv('DB_HOST', 'pgdb'),
#         'PORT': os.getenv('DB_PORT', '5432'),
#     }
# }


DATABASES = {
    'default': {
        'ENGINE': os.getenv('DB_ENGINE', 'django.db.backends.postgresql_psycopg2'),
        'NAME': os.getenv('DB_NAME', 'db1'),
        'USER': os.getenv('DB_USER', 'postgres1'),
        'PASSWORD': os.getenv('DB_USER_PASSWORD', 'postgres1'),
        'HOST': os.getenv('DB_HOST', 'c-c9qi313a1cucdrbehco4.rw.mdb.yandexcloud.net'),
        'PORT': os.getenv('DB_PORT', '6432'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

STATIC_DIR = os.path.join(BASE_DIR, 'static2')
STATIC_URL = '/static2/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static2')
MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'



logger = logging.getLogger(__name__)
logger.debug(f"BASE_DIR: {BASE_DIR}")
logger.debug(f"STATIC_ROOT: {STATIC_ROOT}")
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
    },
}
