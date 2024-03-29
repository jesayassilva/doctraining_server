"""
Django settings for doctraining project.

Generated by 'django-admin startproject' using Django 2.2.5.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os
from decouple import config

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# SESSION_COOKIE_AGE = 86400 # 24 horas * 60 minutos * 60 segundos
SESSION_COOKIE_AGE = 3*24*3600 # 1 hora após sessão para expirar é 3600 seg
# SESSION_EXPIRE_AT_BROWSER_CLOSE = False#Fechar o navegador e sessão expirar
# SESSION_EXPIRE_AT_BROWSER_CLOSE = True#Fechar o navegador e sessão expirar
SESSION_SAVE_EVERY_REQUEST = True#Renova a sessão a cada iteração
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
# DEBUG = config('DEBUG', default=False, cast=bool)

#Modo de teste
# '''
PROJETO_EM_TESTE= False
#True  -> SIM
#False -> NÃO

if(PROJETO_EM_TESTE):
    DEBUG = True
    ALLOWED_HOSTS = ['*']
    ADMINS = [('Jesaias Silva', 'jesayassilva@gmail.com'),('DocTraining', 'doctraining.ufersa@gmail.com')]
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
    }
else:
    # DEBUG = True
    DEBUG = config('DEBUG', default=False, cast=bool)
    ALLOWED_HOSTS = ['doctraining.herokuapp.com','https://doctraining.herokuapp.com']
    # ALLOWED_HOSTS = ['*']
    ADMINS = [('Jesaias Silva', 'jesayassilva@gmail.com'),('DocTraining', 'doctraining.ufersa@gmail.com')]
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': 'd7j8iei44b6dm6',
            'USER': 'hxrxxeccyjhvky',
            'PASSWORD': config('PASSWORD'),
            'HOST': 'ec2-174-129-253-101.compute-1.amazonaws.com',
            'PORT': '5432',
        }
    }


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'doctrainingapp.apps.DoctrainingappConfig',
    'hide_herokuapp'
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


MIDDLEWARE_CLASSES = (
    'hide_herokuapp.middleware.HideHerokuappFromRobotsMiddleware'
)




ROOT_URLCONF = 'doctraining.urls'

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

WSGI_APPLICATION = 'doctraining.wsgi.application'

# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases



# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'pt-br'
TIME_ZONE = 'America/Fortaleza'

LOGIN_URL = "/login/"

LOGIN_REDIRECT_URL = '/doctraining/'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# # EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_HOST = 'smtp.gmail.com'
# EMAIL_HOST_USER = 'doctraining.ufersa.contato@gmail.com'
# EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')
# EMAIL_PORT = 587
# # EMAIL_PORT = 465
# EMAIL_USE_TLS = True
# DEFAULT_FROM_EMAIL = EMAIL_HOST_USER


# SENDGRID_API_KEY = os.getenv('chave_key')

EMAIL_HOST = 'smtp.sendgrid.net'
EMAIL_HOST_USER = 'apikey'
EMAIL_HOST_PASSWORD = config('SEND_GRID_KEY')
EMAIL_PORT = 587
EMAIL_USE_TLS = True






# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

# STATIC_URL = '/static/'
STATIC_ROOT = 'https://jesaias.000webhostapp.com/IBES/static/'
STATIC_URL = 'https://jesaias.000webhostapp.com/IBES/static/'
