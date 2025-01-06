from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-angk520w03#o&^ucga)7#pevu0wyz_so*=ac-y@^#cc+gbv%o+'

DEBUG = False

ALLOWED_HOSTS = ['128.199.26.204',]

# CSRF and Session Configuration
CSRF_COOKIE_SECURE = True  # Ensure CSRF cookie is sent over HTTPS only
CSRF_COOKIE_SAMESITE = 'None'  # For cross-site cookies (works on mobile and desktop)
CSRF_TRUSTED_ORIGINS = ['http://128.199.26.204', 'https://128.199.26.204']  # Include both HTTP and HTTPS

SESSION_COOKIE_SECURE = True  # Ensure session cookies are sent over HTTPS only
SESSION_COOKIE_SAMESITE = 'None'  # For cross-site session cookies (works on mobile and desktop)

# CORS Settings (for AJAX/requests from other origins)
CORS_ALLOW_ALL_ORIGINS = True  # Allow all origins (you can customize this based on your needs)
CORS_ALLOWED_ORIGINS = [
    'http://128.199.26.204',
    'https://128.199.26.204',
]

# Middleware Settings
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

INSTALLED_APPS = [
    'whitenoise.runserver_nostatic',  
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'eff_apps',
]

# Static and Media Files Configuration
STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Database Settings
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': 'debug.log',
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}

# Template Configuration
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['templates'],
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

# WSGI Application
WSGI_APPLICATION = 'efficient_corporates.wsgi.application'

# Site Configuration
SITE_ID = 1
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Kolkata'
USE_I18N = True
USE_TZ = True

# Password Validation
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Security Settings
SECURE_SSL_REDIRECT = True  # Redirect HTTP to HTTPS in production
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')  # For setups behind a proxy/load balancer
X_FRAME_OPTIONS = 'DENY'  # Prevent embedding site in iframes (clickjacking protection)

# Custom Redirect URL for Payment and Webhooks (if applicable)
DJANGO_CUSTOM_REDIRECT_URL = "http://128.199.26.204/payment-status/"
DJANGO_CUSTOM_CALLBACK_URL = "http://128.199.26.204/webhook/"

