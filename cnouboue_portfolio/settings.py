"""
Django settings for cnouboue_portfolio project.

Generated by 'django-admin startproject' using Django 2.0.6.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.0/ref/settings/
"""

import os
import django_heroku
import dj_database_url


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATES_DIR = os.path.join(BASE_DIR, "templates")

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
# SECRET_KEY = '9d28q_#wtk0q4pvgm*+=hkd*^42j_2a#*13x^&c*f=oos)fykf'
# SECRET_KEY = os.environ.get('SECRET_KEY', '9d28q_#wtk0q4pvgm*+=hkd*^42j_2a#*13x^&c*f=oos)fykf') # development key for the moment

# SECURITY WARNING: don't run with debug turned on in production!

"""
if os.environ.get("environement") == "PRODUCTION":
    DEBUG = True
    # SECRET_KEY = os.environ.get('SECRET_KEY')
    SECRET_KEY = "9d28q_#wtk0q4pvgm*+=hkd*^42j_2a#*13x^&c*f=oos)fykf"
    SESSION_COOKIE_SECURE = True

else:
    DEBUG = True
    SECRET_KEY = "9d28q_#wtk0q4pvgm*+=hkd*^42j_2a#*13x^&c*f=oos)fykf"
    SESSION_COOKIE_SECURE = False
"""

DEBUG = int(os.environ.get("DEBUG", default=1))

SECRET_KEY = os.environ.get("SECRET_KEY", "default_key")

ADMINS = [("cyrilhokage", "cyrillenouboue@gmail.com")]
MANAGERS = ADMINS


SESSION_COOKIE_SECURE = False

ALLOWED_HOSTS = [
    "127.0.0.1",
    ".cyrillenouboue.space",
    "192.168.1.13",
]

CSRF_COOKIE_SECURE = True

# Application definition

INSTALLED_APPS = [
    "notebook.apps.NotebookConfig",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sitemaps",
    "django.contrib.humanize",
    "django.contrib.sites",
    "blog",
    "crispy_forms",
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "allauth.socialaccount.providers.google",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

"""
if os.environ.get("environement") == "PRODUCTION":
    # ...
    # Simplified static file serving.
    # https://warehouse.python.org/project/whitenoise/
    STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"
    """

STATICFILES_STORAGE = "whitenoise.storage.CompressedStaticFilesStorage"

ROOT_URLCONF = "cnouboue_portfolio.urls"


TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [TEMPLATES_DIR],
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

WSGI_APPLICATION = "cnouboue_portfolio.wsgi.application"


# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

if os.getenv("GITHUB_WORKFLOW"):
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": "github-actions",
            "USER": "postgres",
            "PASSWORD": "postgres",
            "HOST": "localhost",
            "PORT": "5432",
        }
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": os.environ.get("SQL_ENGINE", "django.db.backends.sqlite3"),
            "NAME": os.environ.get(
                "SQL_DATABASE", os.path.join(BASE_DIR, "db.sqlite3")
            ),
            "USER": os.environ.get("SQL_USER", "user"),
            "PASSWORD": os.environ.get("SQL_PASSWORD", "password"),
            "HOST": os.environ.get("SQL_HOST", "localhost"),
            "PORT": os.environ.get("SQL_PORT", "5432"),
        }
    }


# ...
"""
if os.environ.get('ENV') == 'PRODUCTION':
    # ...
    db_from_env = dj_database_url.config(conn_max_age=500)
    DATABASES['default'].update(db_from_env)
"""

# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators

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

# Looging configuration


LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s",
            "datefmt": "%d/%b/%Y %H:%M:%S",
        },
        "simple": {"format": "%(levelname)s %(message)s"},
    },
    "handlers": {
        "file": {
            "level": "DEBUG",
            "class": "logging.FileHandler",
            "filename": os.path.join(BASE_DIR, "django.log"),
            "formatter": "verbose",
        },
    },
    "loggers": {
        "django": {
            "handlers": ["file"],
            "propagate": True,
            "level": "DEBUG",
        },
        "blog": {
            "handlers": ["file"],
            "level": "DEBUG",
        },
        "notebook": {
            "handlers": ["file"],
            "level": "DEBUG",
        },
    },
}


# Internationalization
# https://docs.djangoproject.com/en/2.0/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/

STATIC_URL = "/static/"
STATICFILES_DIRS = (os.path.join(BASE_DIR, "static"),)
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

if os.environ.get("ENV") == "PRODUCTION":

    # BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    STATIC_URL = "/static/"
    STATICFILES_DIRS = (os.path.join(BASE_DIR, "static"),)

    # Static files settings
    # PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

    # STATIC_ROOT = os.path.join(PROJECT_ROOT, 'staticfiles')

    # Extra places for collectstatic to find static files.
    # STATICFILES_DIRS = (
    #   os.path.join(PROJECT_ROOT, 'static'),
    # )

# Configure the media base dir and medias urls
MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

COLLECTSTATIC = 1


# Activate Django-Heroku.
django_heroku.settings(locals())

SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
CRISPY_TEMPLATE_PACK = "bootstrap4"
LOGIN_REDIRECT_URL = "notebook:profile-user"
LOGIN_URL = "notebook:login"

# SESSION_ENGINE = 'django.contrib.sessions.backends.db'
# Password reset email
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_USE_TLS = True

SITE_ID = 2

EMAIL_HOST_USER = os.environ.get("EMAIL_APP_ID", "notebookapp20@gmail.com")
EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_PASSWORD")

AUTHENTICATION_BACKENDS = (
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
)


SOCIALACCOUNT_PROVIDERS = {
    "google": {
        "SCOPE": [
            "profile",
            "email",
        ],
        "AUTH_PARAMS": {
            "access_type": "online",
        },
    }
}
