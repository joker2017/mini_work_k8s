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

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-jdk9%)1!9grg$5q3@*v5*%4vh5b$_ns@(#g9&o@#mb-df9!8z0'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['*', 'localhost']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'account',
    'flags',
    'rest_framework',
    'django.contrib.postgres', 

]

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


# Database


# For PosgreSQL
# DATABASES = {
#     'default': {
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


FLAGS = {
'ACCOUNT_LIST_FLAG': [],
'ACCOUNT_CREATE_FLAG': [],
'ACCOUNT_UPDATE_FLAG': [],
'ACCOUNT_DESTROY_FLAG': [],
'USERS_DESTROY_FLAG': [],
'ACCOUNT_DETAIL_FLAG': [],
}



CSRF_TRUSTED_ORIGINS = ['https://bmini.ru/', 'http://bmini.ru/']
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


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

#STATIC_URL = "/static1/"
#STATIC_ROOT = os.path.join(BASE_DIR, "static")

STATIC_DIR = os.path.join(BASE_DIR, 'static1')
STATIC_URL = '/static1/'
#STATICFILES_DIRS = [STATIC_DIR,]
STATIC_ROOT = os.path.join(BASE_DIR, 'static1')

MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")


#MEDIA_ROOT = '/vol/web/media'
#STATIC_ROOT = '/vol/web/static'


# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
print(f"BASE_DIR: {BASE_DIR}")
print(f"STATIC_ROOT: {STATIC_ROOT}")
import logging
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
            'level': 'DEBUG',  # Измените уровень логирования здесь
        },
    },
}
