import os
from os import getenv
from pathlib import Path
import environ
import dj_database_url
from django.core.management.utils import get_random_secret_key

# Environment variables
environ.Env.read_env()

# Usar servicios de AWS, si no usa gratuitos
USE_AWS_SERVICES = False # S3, SES, etc.

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Production Settings
SECRET_KEY = getenv('SECRET_KEY', get_random_secret_key())
DEBUG = getenv('DEBUG', 'False') == 'True'

ALLOWED_HOSTS = '127.0.0.1,localhost'.split(',')
if not DEBUG:
    ALLOWED_HOSTS = getenv('ALLOWED_HOSTS_DEPLOY').split(',')

# Render Hostnames
RENDER_EXTERNAL_HOSTNAME = os.environ.get('RENDER_EXTERNAL_HOSTNAME')
if RENDER_EXTERNAL_HOSTNAME:
    ALLOWED_HOSTS.append(RENDER_EXTERNAL_HOSTNAME)

# Application definition
DJANGO_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

PROJECT_APPS = [
    'apps.user'
]

THIRD_PARTY_APPS = [
    'rest_framework',
    'djoser',
    'social_django',
    #'django_ses',
    'corsheaders',
]

INSTALLED_APPS = DJANGO_APPS + PROJECT_APPS + THIRD_PARTY_APPS

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    'whitenoise.middleware.WhiteNoiseMiddleware',
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "core.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
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

WSGI_APPLICATION = "core.wsgi.application"


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

if not DEBUG:
    DATABASES = {
        'default': dj_database_url.config(
            # Feel free to alter this value to suit your needs.
            default='sqlite:///db.sqlite3',
            conn_max_age=600
        )
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True


# Static files (CSS, JavaScript, Images)
STATIC_URL = "static/"

if not DEBUG:
    STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
    STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
else:
    STATIC_ROOT = BASE_DIR / 'static'

MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Default primary key field type
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


###########################################   Authentication   ###########################################
AUTH_USER_MODEL = 'user.UserAccount'

AUTH_COOKIE = 'access'
AUTH_COOKIE_ACCESS_MAX_AGE = 60 * 5 # 60 seg x 5
AUTH_COOKIE_REFRESH_MAX_AGE = 60 * 60 * 24

AUTH_COOKIE_PATH = '/'
AUTH_COOKIE_SAMESITE = None

AUTH_COOKIE_HTTP_ONLY = True

AUTH_COOKIE_SECURE = False
if not DEBUG:
    AUTH_COOKIE_SECURE = getenv('AUTH_COOKIE_SECURE') == 'True'

# Social Authentication
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = getenv('GOOGLE_AUTH_KEY')
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = getenv('GOOGLE_AUTH_SECRET_KEY')
SOCIAL_AUTH_GOOGLE_OAUTH2_SCOPE = [
    'https://www.googleapis.com/auth/userinfo.email',
    'https://www.googleapis.com/auth/userinfo.profile',
    'openid'
]
SOCIAL_AUTH_GOOGLE_OAUTH2_EXTRA_DATA = ['first_name', 'last_name']

SOCIAL_AUTH_FACEBOOK_KEY = getenv('FACEBOOK_AUTH_KEY')
SOCIAL_AUTH_FACEBOOK_SECRET = getenv('FACEBOOK_AUTH_SECRET_KEY')
SOCIAL_AUTH_FACEBOOK_SCOPE = ['email']
SOCIAL_AUTH_FACEBOOK_PROFILE_EXTRA_PARAMS = {
    'fields': 'email, first_name, last_name'
}


# Authentication Backends
AUTHENTICATION_BACKENDS = [
    'social_core.backends.google.GoogleOAuth2',
    'social_core.backends.facebook.FacebookOAuth2',
    'django.contrib.auth.backends.ModelBackend',
]


# Cors Headers Settings
CORS_ORIGIN_WHITELIST = [
    'http://localhost:3000',
    'http://localhost:8000',
]

CSRF_TRUSTED_ORIGINS = [
    'http://localhost:3000',
    'http://localhost:8000',
]

CORS_ALLOW_CREDENTIALS = True

if not DEBUG:
    CORS_ORIGIN_WHITELIST = getenv('CORS_ORIGIN_WHITELIST').split(',')
    CSRF_TRUSTED_ORIGINS = getenv('CSRF_TRUSTED_ORIGINS').split(',')


# Django Rest Framework
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'apps.user.authentication.JWTAuthentication',
    ],

    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated'
    ]
}


# Djoser Authentication
DJOSER = {
    'PASSWORD_RESET_CONFIRM_URL': 'password-reset/{uid}/{token}',
    'SEND_ACTIVATION_EMAIL': True,
    'ACTIVATION_URL': 'activate/{uid}/{token}',
    'USER_CREATE_PASSWORD_RETYPE': True,
    'SET_PASSWORD_RETYPE': True,
    'PASSWORD_RESET_CONFIRM_RETYPE': True,
    'TOKEN_MODEL': None,
    'SOCIAL_AUTH_ALLOWED_REDIRECT_URIS': \
        getenv('REDITECT_URLS_DEPLOY').split(',')\
        if DEBUG == False else getenv('REDITECT_URLS_LOCAL').split(',')

}

# Djoser Email Templates
DOMAIN = '127.0.0.1:3000'
SITE_NAME= 'Auth-Test'

if not DEBUG:
    DOMAIN = getenv('DOMAIN')
    SITE_NAME= getenv('SITE_NAME')


# Email settings
EMAIL_BACKEND='django.core.mail.backends.console.EmailBackend'

if USE_AWS_SERVICES:
    EMAIL_BACKEND = 'django_ses.SESBackend'
    DEFAULT_FROM_EMAIL = getenv('AWS_SES_FROM_EMAIL')

    AWS_SES_ACCESS_KEY_ID = getenv('AWS_SES_ACCESS_KEY_ID')
    AWS_SES_SECRET_ACCESS_KEY = getenv('AWS_SES_SECRET_ACCESS_KEY')
    AWS_SES_REGION_NAME = getenv('AWS_SES_REGION_NAME')
    AWS_SES_REGION_ENDPOINT = f'email.{AWS_SES_REGION_NAME}.amazonaws.com'
    AWS_SES_FROM_EMAIL = getenv('AWS_SES_FROM_EMAIL')
    USE_SES_V2 = True
else:
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
    EMAIL_HOST = 'smtp.resend.com'
    EMAIL_PORT = 587  # El puerto puede variar según el servidor SMTP
    EMAIL_USE_TLS = True  # Usar TLS si el servidor lo requiere
    EMAIL_HOST_USER = 'resend'
    EMAIL_HOST_PASSWORD = getenv('EMAIL_HOST_PASSWORD')
    DEFAULT_FROM_EMAIL = "test-auth <noreply@gastonfr.com>"


USER_CREATION_PASSWORD = getenv('USER_CREATION_PASSWORD')
