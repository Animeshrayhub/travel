"""
Ma Mangala Travels - Django Settings
Supports both local development and Vercel (production) deployment.
"""

import os
from pathlib import Path
from django.contrib.messages import constants as msg_constants

# Build paths — BASE_DIR = d:\tisha (or /var/task on Vercel)
BASE_DIR = Path(__file__).resolve().parent.parent

# ─── Security ────────────────────────────────
# In production, set SECRET_KEY as an environment variable on Vercel dashboard
SECRET_KEY = os.environ.get(
    'SECRET_KEY',
    'django-insecure-mamangala-travels-odisha-secret-key-2024'
)

# DEBUG: False in production. Set DJANGO_DEBUG=False on Vercel env vars.
DEBUG = os.environ.get('DJANGO_DEBUG', 'True') == 'True'

# Vercel domain + custom domain go here
ALLOWED_HOSTS = os.environ.get(
    'ALLOWED_HOSTS',
    '*'
).split(',')


# ─── Installed Apps ──────────────────────────
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'travels',  # Ma Mangala Travels app
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    # WhiteNoise: serves static files on Vercel (no web server needed)
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'ma_mangala_travels.urls'

# ─── Templates ───────────────────────────────
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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

WSGI_APPLICATION = 'ma_mangala_travels.wsgi.application'


# ─── Database ────────────────────────────────
# On Vercel, BASE_DIR resolves to /var/task which is READ-ONLY.
# We detect this by path prefix and redirect SQLite to writable /tmp.
# On Windows/local, BASE_DIR is d:\tisha so we use it directly.
_ON_VERCEL = str(BASE_DIR).startswith('/var/')
DB_PATH = Path('/tmp/db.sqlite3') if _ON_VERCEL else BASE_DIR / 'db.sqlite3'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': DB_PATH,
    }
}


# ─── Password Validation ─────────────────────
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]


# ─── Localisation ────────────────────────────
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Kolkata'
USE_I18N = True
USE_TZ = True


# ─── Static Files (WhiteNoise handles serving on Vercel) ─────────────────────
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'

# WhiteNoise compressed caching for production
STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}


# ─── Media Files ─────────────────────────────
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'


# ─── Default Primary Key ─────────────────────
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# ─── Message Tags (Bootstrap compatible) ─────
MESSAGE_TAGS = {
    msg_constants.DEBUG: 'secondary',
    msg_constants.INFO: 'info',
    msg_constants.SUCCESS: 'success',
    msg_constants.WARNING: 'warning',
    msg_constants.ERROR: 'danger',
}


# ─── CSRF trusted origins (Vercel URLs) ───────
CSRF_TRUSTED_ORIGINS = os.environ.get(
    'CSRF_TRUSTED_ORIGINS',
    'http://localhost:8000,http://127.0.0.1:8000'
).split(',')
