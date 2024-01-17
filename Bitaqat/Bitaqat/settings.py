"""
Django settings for Bitaqat project.

Generated by 'django-admin startproject' using Django 4.1.4.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""

from pathlib import Path
import os
import environ
env = environ.Env()

environ.Env.read_env()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env("DJANGO_SK")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = 'False'

ALLOWED_HOSTS = ["Bitaqat-1-dev.us-west-2.elasticbeanstalk.com","127.0.0.1"]


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "authentication",
    "Club",
    "Fan",
    'silk',
    "compressor",
    'storages'
]
SILKY_PYTHON_PROFILER = True

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder',
)

MIDDLEWARE = [
    'django.middleware.gzip.GZipMiddleware',
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    'silk.middleware.SilkyMiddleware',
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",

]

COMPRESS_ENABLED = True
COMPRESS_OFFLINE = True
COMPRESS_OUTPUT_DIR = 'compressed'

COMPRESS_JS_FILTERS = [
    'compressor.filters.jsmin.JSMinFilter',
    'compressor.filters.uglifyjs.UglifyJSFilter',
]

ROOT_URLCONF = "Bitaqat.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": ['authentication/templates/authentication', 'Club/templates/Club', 'Fan/templates/Fan'],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'unique-snowflake',
    }
}

WSGI_APPLICATION = "Bitaqat.wsgi.application"

SESSION_EXPIRE_AT_BROWSER_CLOSE = False
SESSION_COOKIE_AGE = 60*60
# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'Bitaqat-v1',
        'USER': 'postgres',
        'PASSWORD': 'Jihad2002',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}
# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


AUTH_USER_MODEL = 'authentication.myUsers'

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend'
]

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Baghdad'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/
STATICFILES_DIRS = [
    # Joining the BASE_DIR with the string "SignUpAuth\static"
    os.path.join(BASE_DIR, "authentication/static"),
    os.path.join(BASE_DIR, "Club/static"),
    os.path.join(BASE_DIR, "Fan/static"),
]
# Uncomment for AWS
# STATIC_ROOT = os.path.join(BASE_DIR, "..", "www", "static")

STATIC_ROOT = os.path.join(BASE_DIR, 'assetsfinal')
STATIC_URL = '/static/'

STATICFILES_LOCATION = 'static'


MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, "static/media")

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


INTERNAL_IPS = [
    '127.0.0.1'
]


# DEBUG_TOOLBAR_CONFIG = {
#     "SHOW_TOOLBAR_CALLBACK": lambda request: True,
# }

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.live.com'  # For Hotmail/Outlook
EMAIL_PORT = 587  # For TLS
EMAIL_USE_TLS = True

# AWS_STORAGE_BUCKET_NAME = 'bitaqatbucket'
# AWS_S3_REGION_NAME = 'eu-north-1'  # e.g. us-east-2
# AWS_ACCESS_KEY_ID = 'AKIAYF3FRH75DISKMNP5'
# AWS_SECRET_ACCESS_KEY = 'mFVzij1aHxXxPAQnzUxaNT8EtF+JzV0BY4iBL7lj'

# # Tell django-storages the domain to use to refer to static files.
# AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME

# # Tell the staticfiles app to use S3Boto3 storage when writing the collected static files (when
# # you run `collectstatic`).
# STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

# DEFAULT_FILE_STORAGE  = 'storages.backends.s3boto3.S3Boto3Storage'