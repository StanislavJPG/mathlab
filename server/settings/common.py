"""
Django settings for mathlab project.

Generated by 'django-admin startproject' using Django 5.0.3.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""

import logging.config
import sys
from pathlib import Path
import os

from django.urls import reverse_lazy
from django.contrib.messages import constants as messages

from dotenv import load_dotenv

from .celery import *  # noqa: F403

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


load_dotenv()
DEFAULT_ADMIN_TOKEN = os.getenv('DEFAULT_ADMIN_TOKEN')


# Application definition

INSTALLED_APPS = [
    # django's
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # installed packages
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    'channels',
    'widget_tweaks',
    'tinymce',
    'easy_thumbnails',
    'hitcount',
    'django_countries',
    'django_cleanup.apps.CleanupConfig',
    # common
    'server.common',
    # apps
    'server.apps.explainme.apps.ExplainmeConfig',
    'server.apps.solvexample.apps.SolvexampleConfig',
    'server.apps.graphbuilder.apps.GraphbuilderConfig',
    'server.apps.forum.apps.ForumConfig',
    'server.apps.users.apps.UsersConfig',
    'server.apps.math_news.apps.MathNewsConfig',
    'server.apps.chat.apps.ChatConfig',
    'server.apps.theorist.apps.TheoristConfig',
    # templatetags
    'server.common.templatetags.widened_widget_tweaks',
    'server.common.templatetags.avatars',
]


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    # installed packages
    'allauth.account.middleware.AccountMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django_htmx.middleware.HtmxMiddleware',
    # custom middlewares
    'server.common.middlewares.HTMXToastMiddleware',
    'server.common.middlewares.UnifiedRequestMiddleware',
    'server.common.middlewares.OnboardingMiddleware',
]

ROOT_URLCONF = 'server.urls.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates', BASE_DIR / 'apps'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.i18n',
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ]
        },
    },
]


WSGI_APPLICATION = 'server.settings.wsgi.application'

FIXTURE_DIRS = [
    os.path.join(BASE_DIR.parent, 'data', 'fixtures'),  # Global fixtures directory
]

# RENDER DATABASE

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DB_NAME'),
        'USER': os.getenv('DB_USER'),
        'PASSWORD': os.getenv('DB_PASS'),
        'HOST': os.getenv('DB_HOST'),
        'PORT': os.getenv('DB_PORT'),
    }
}

# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

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

AUTHENTICATION_BACKENDS = [
    # Needed to login by username in Django admin, regardless of `allauth`
    'django.contrib.auth.backends.ModelBackend',
    # `allauth` specific authentication methods, such as login by email
    'allauth.account.auth_backends.AuthenticationBackend',
]

SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'APP': {
            'client_id': os.getenv('GOOGLE_AUTH_WEB_CLIENT_ID'),
            'secret': os.getenv('GOOGLE_AUTH_WEB_CLIENT_SECRET'),
            'key': '',
        },
        'SCOPE': [
            'profile',
            'email',
        ],
        'AUTH_PARAMS': {
            'access_type': 'offline',
        },
        'OAUTH_PKCE_ENABLED': True,
    }
}

ACCOUNT_ADAPTER = 'server.apps.users.adapters.AccountAdapter'
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_LOGIN_METHODS = {'email'}
ACCOUNT_EMAIL_VERIFICATION = 'none'  # TODO: remove this var if not debug

SOCIALACCOUNT_AUTO_SIGNUP = True
SOCIALACCOUNT_ADAPTER = 'server.apps.users.adapters.SocialAccountAdapter'

AUTH_USER_MODEL = 'users.CustomUser'

ACCOUNT_SIGNUP_REDIRECT_URL = reverse_lazy('theorist_onboarding:base-page')
LOGIN_REDIRECT_URL = reverse_lazy('forum:base-forum-page')
ACCOUNT_LOGOUT_REDIRECT_URL = reverse_lazy('forum:base-forum-page')

ACCOUNT_FORMS = {
    'reset_password': 'server.apps.users.forms.CustomResetPasswordForm',
}

LOGIN_URL = reverse_lazy('users:base-auth')

SITE_ID = 1
SITE_DEFAULT_URL = reverse_lazy('forum:base-forum-page')

# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'uk'
LANGUAGES = [
    ('en', 'English'),
    ('uk', 'Ukrainian'),
]
USE_I18N = True
USE_TZ = True

LOCALE_PATHS = [
    BASE_DIR.parent / 'locale',
]

MEDIA_ROOT = ''

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = '/static/'

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

TINYMCE_DEFAULT_CONFIG = {
    'theme': 'silver',
    'height': 400,
    'menubar': False,
    'setup': """
    function(editor) {
        editor.on('blur', function() { editor.save(); });
        editor.on('focusout', function() { editor.save(); });
        editor.on('touchend', function() { editor.save(); });
    }
    """,  # that fixes bug with HTMX + TinyMCE
    'plugins': 'advlist,autolink,lists,link,image,charmap,preview,anchor,'
    'searchreplace,visualblocks,code,fullscreen,insertdatetime,media,table,'
    'code,help,wordcount',
    'toolbar': 'undo redo | formatselect | '
    'bold italic backcolor | alignleft aligncenter '
    'alignright alignjustify | bullist numlist outdent indent | '
    'removeformat | help',
}

MESSAGE_TAGS = {messages.ERROR: 'danger', messages.SUCCESS: 'success'}

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_HOST_USER = os.getenv('MAIL_NAME')
EMAIL_HOST_PASSWORD = os.getenv('MAIL_PASS')

TIME_ZONE = 'Europe/Kiev'

CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': f'redis://redis:{os.getenv("REDIS_PORT")}',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        },
    }
}

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'stream': sys.stdout,
        },
    },
    'root': {'handlers': ['console'], 'level': 'INFO'},
}
logging.config.dictConfig(LOGGING)

# ELASTICSEARCH_DSL = {
#     'default': {
#         'hosts': os.getenv('ELASTICSEARCH_HOST'),
#         'http_auth': (os.getenv('ELASTICSEARCH_NAME'), os.getenv('ELASTICSEARCH_PASS'))
#     }
# }


CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            'hosts': [('redis', os.getenv('REDIS_PORT'))],
        },
    },
}

ASGI_APPLICATION = 'server.apps.chat.routing.application'
