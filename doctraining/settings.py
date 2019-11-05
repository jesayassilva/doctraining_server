"""
Django settings for doctraining project.

Generated by 'django-admin startproject' using Django 2.2.5.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
# SECRET_KEY = config('SECRET_KEY')
SECRET_KEY = 'i96expt%3unxb1jb826onbqdl^@ke3+0s7mojx--=^lc92@+d!'



# SECURITY WARNING: don't run with debug turned on in production!
# DEBUG = config('DEBUG', default=False, cast=bool)

# DEBUG = True
DEBUG = False

ALLOWED_HOSTS = ['doctraining.herokuapp.com','https://doctraining.herokuapp.com']
# ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'doctrainingapp.apps.DoctrainingappConfig'
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

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'd7j8iei44b6dm6',
        'USER': 'hxrxxeccyjhvky',
        'PASSWORD': 'd19b0eb8138f99c5ed12eef3ed1740dff036df5a16eafd8f678e8563be8eb2ea',
        'HOST': 'ec2-174-129-253-101.compute-1.amazonaws.com',
        'PORT': '5432',
    }
}



# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#     }
# }


# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.p',
#         'HOST':'10.5.0.187',
#         'PASSWORD':'z800lesi514',
#         'USER':'root',
#         'NAME':'doctrainingmobile',
#         'PORT':'3306',
#         'OPTIONS': {
#           'autocommit': True,
#         },
#
#     }
# }


# DATABASES = {
#     'default': {
#         'ENGINE':'mysql.connector.django',
#         # 'ENGINE': 'django.db.backends.mysql',
#         'HOST':'doctraining2.mysql.uhserver.com',
#         'PASSWORD':'docles2019*',
#         'USER':'mod_inteligente',
#         'NAME':'doctraining2',
#         'PORT':'3306',
#         'OPTIONS': {
#                   'autocommit': True,
#                 },
#     }
# }


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

LOGIN_REDIRECT_URL = '/salas/todas/'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

# STATIC_URL = '/static/'
STATIC_ROOT = 'https://jesaias.000webhostapp.com/IBES/static/'
STATIC_URL = 'https://jesaias.000webhostapp.com/IBES/static/'
