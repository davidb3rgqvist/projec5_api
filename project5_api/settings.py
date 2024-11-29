"""
Django settings for project5_api project.

Generated by 'django-admin startproject' using Django 5.1.1.
"""
from pathlib import Path
import os
import dj_database_url
import datetime

# Load environment variables
if os.path.exists('env.py'):
    import env

# Cloudinary storage setup
CLOUDINARY_STORAGE = {
    'CLOUDINARY_URL': os.environ.get('CLOUDINARY_URL')
}
MEDIA_URL = '/media/'
DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'

# Base directory for the project
BASE_DIR = Path(__file__).resolve().parent.parent

# REST Framework settings
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [(
        'rest_framework.authentication.SessionAuthentication'
        if 'DEV' in os.environ
        else 'dj_rest_auth.jwt_auth.JWTCookieAuthentication'
    )],
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.SearchFilter',
    ],
    'DEFAULT_PAGINATION_CLASS': (
        'rest_framework.pagination.PageNumberPagination'
    ),
    'PAGE_SIZE': 10,
    'DATETIME_FORMAT': '%d %b %Y',
}

# CSRF trusted origins
CSRF_TRUSTED_ORIGINS = [
  "https://3000-davidb3rgqv-project5foo-75up2jzyvte.ws.codeinstitute-ide.net",
  "https://8000-davidb3rgqv-project5api-dff603ub8x0.ws.codeinstitute-ide.net",
]

# JWT authentication settings
REST_USE_JWT = True
JWT_AUTH_SECURE = True
JWT_AUTH_COOKIE = 'my-app-auth'
JWT_AUTH_REFRESH_COOKIE = 'my-refresh-token'
JWT_AUTH_SAMESITE = 'None'
JWT_AUTH = {
    'JWT_EXPIRATION_DELTA': datetime.timedelta(days=10),
    'JWT_REFRESH_EXPIRATION_DELTA': datetime.timedelta(days=30),
}

# Authentication serializers
REST_AUTH_SERIALIZERS = {
    'USER_DETAILS_SERIALIZER': 'project5_api.serializers.CurrentUserSerializer'
}

# Only allow JSON rendering in production
if 'DEV' not in os.environ:
    REST_FRAMEWORK['DEFAULT_RENDERER_CLASSES'] = [
        'rest_framework.renderers.JSONRenderer',
    ]

# Secret key management
SECRET_KEY = os.environ.get('SECRET_KEY')

# Debug mode based on environment
DEBUG = 'DEV' in os.environ

# Allowed hosts
ALLOWED_HOSTS = [
    '8000-davidb3rgqv-project5api-dff603ub8x0.ws.codeinstitute-ide.net',
    '127.0.0.1:8000',
    'foorky-fe-79ffc00345fc.herokuapp.com',
    'project5-api-a299de19cbb3.herokuapp.com',
    'localhost'
]

# Application definition
INSTALLED_APPS = [
    # Default Django apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'cloudinary_storage',
    'django.contrib.staticfiles',
    'cloudinary',
    'rest_framework',
    'django_filters',
    'rest_framework.authtoken',
    'dj_rest_auth',
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'dj_rest_auth.registration',
    'corsheaders',

    # Custom apps
    'profiles',
    'recipes',
    'likes',
    'followers',
]
SITE_ID = 1

# Middleware
MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# CORS settings
if 'CLIENT_ORIGIN' in os.environ:
    CORS_ALLOWED_ORIGINS = [
        os.environ.get('CLIENT_ORIGIN')
    ]
else:
    CORS_ALLOWED_ORIGIN_REGEXES = [
        r"^https://.*\.gitpod\.io$",
        r"^https://.*\.codeinstitute\.net$",
    ]

CORS_ALLOWED_ORIGINS = [
    'https://3000-davidb3rgqv-project5foo-75up2jzyvte.ws.codeinstitute-ide.net',
    'https://foorky-fe-79ffc00345fc.herokuapp.com',
    'https://project5-api-a299de19cbb3.herokuapp.com'
]

CORS_ALLOW_CREDENTIALS = True

# URL configuration
ROOT_URLCONF = 'project5_api.urls'

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

# WSGI application
WSGI_APPLICATION = 'project5_api.wsgi.application'

# Database configuration
if 'DEV' in os.environ:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }
else:
    DATABASES = {
        'default': dj_database_url.parse(os.environ.get("DATABASE_URL"))
    }

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': (
            'django.contrib.auth.password_validation.'
            'UserAttributeSimilarityValidator'
        ),
    },
    {
        'NAME': (
            'django.contrib.auth.password_validation.'
            'MinimumLengthValidator'
        ),
    },
    {
        'NAME': (
            'django.contrib.auth.password_validation.'
            'CommonPasswordValidator'
        ),
    },
    {
        'NAME': (
            'django.contrib.auth.password_validation.'
            'NumericPasswordValidator'
        ),
    },
]

# Internationalization settings
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static files
STATIC_URL = 'static/'

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
