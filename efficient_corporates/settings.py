from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-angk520w03#o&^ucga)7#pevu0wyz_so*=ac-y@^#cc+gbv%o+'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['128.199.26.204']  # Update with your actual production host(s)

# Application definition
INSTALLED_APPS = [
    'whitenoise.runserver_nostatic',  # For serving static files in production
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'eff_apps',  # Replace with your actual app name
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # For static files management in production
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'efficient_corporates.urls'

# Database settings
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',  # Change to PostgreSQL, MySQL, etc., for production
        'NAME': BASE_DIR / 'db.sqlite3',  # Change path for production database
    }
}

# CSRF settings
CSRF_TRUSTED_ORIGINS = ['http://128.199.26.204', 'https://128.199.26.204']  # Add all trusted origins
CSRF_COOKIE_SECURE = True  # Secure CSRF cookie in production
SESSION_COOKIE_SECURE = True  # Secure session cookie in production

# Security settings
SECURE_SSL_REDIRECT = True  # Force all HTTP requests to redirect to HTTPS
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')  # For setups behind a proxy/load balancer
X_FRAME_OPTIONS = 'DENY'  # Protect against clickjacking
SECURE_HSTS_SECONDS = 31536000  # HTTP Strict Transport Security (HSTS)
SECURE_HSTS_INCLUDE_SUBDOMAINS = True  # Include subdomains in HSTS
SECURE_HSTS_PRELOAD = True  # Preload HSTS

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Kolkata'
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, images)
STATIC_URL = 'static/'

STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# To collect static files during deployment (run `python manage.py collectstatic`)
# Make sure your static files are configured properly for production

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Logging settings
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
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
        'wallet': {  # Custom logger for your app
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': False,
        },
    },
}


MERCHANT_ID="PGTESTPAYUAT140"
PHONE_PE_SALT="775765ff-824f-4cc4-9053-c3926e493514"
PHONE_PE_HOST="https://api-preprod.phonepe.com/apis/pg-sandbox"
# Custom Redirect and Callback URLs for payment integration
DJANGO_CUSTOM_REDIRECT_URL = "http://128.199.26.204/payment-status/"
DJANGO_CUSTOM_CALLBACK_URL = "http://128.199.26.204/webhook/"

# Add any other settings specific to your production environment
