import os

from bleach import sanitizer
from django.urls import reverse_lazy

# ALLAUTH

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
ACCOUNT_LOGIN_METHODS = {'email'}
ACCOUNT_SIGNUP_FIELDS = ['email*', 'username*', 'password1*', 'password2*']
ACCOUNT_EMAIL_VERIFICATION = 'none' if os.getenv('DJANGO_ENV') == 'dev' else 'optional'

SOCIALACCOUNT_AUTO_SIGNUP = True
SOCIALACCOUNT_ADAPTER = 'server.apps.users.adapters.SocialAccountAdapter'
ACCOUNT_SIGNUP_REDIRECT_URL = reverse_lazy('theorist_onboarding:base-page')
LOGIN_REDIRECT_URL = reverse_lazy('forum:base-forum-page')
ACCOUNT_LOGOUT_REDIRECT_URL = reverse_lazy('forum:base-forum-page')

ACCOUNT_FORMS = {
    'login': 'server.apps.users.forms.CustomLoginForm',
    'change_password': 'server.apps.users.forms.CustomPasswordChangeForm',
    'reset_password': 'server.apps.users.forms.CustomResetPasswordForm',
}

# HONEYPOT

HONEYPOT_FIELD_NAME = 'phonenumber'

# NOTIFICATIONS

NOTIFICATIONS_NOTIFICATION_MODEL = 'theorist_notifications.TheoristNotification'
DJANGO_NOTIFICATIONS_CONFIG = {'SOFT_DELETE': True}

# TINYMCE

TINYMCE_DEFAULT_CONFIG = {
    'theme': 'silver',
    'selector': 'textarea',
    'height': 250,
    'menubar': False,
    'setup': """
    function(editor) {
        editor.on('blur', function() { editor.save(); });
        editor.on('focusout', function() { editor.save(); });
        editor.on('touchend', function() { editor.save(); });
    }
    """,  # that fixes bug with HTMX + TinyMCE
    'plugins': 'eqneditor,advlist,autolink,lists,link,image,charmap,preview,anchor,'
    'searchreplace,visualblocks,code,fullscreen,insertdatetime,media,table,'
    'code,help,wordcount',
    'toolbar': 'undo redo | formatselect | eqneditor |'
    'bold italic backcolor | alignleft aligncenter '
    'alignright alignjustify | bullist numlist outdent indent | '
    'removeformat | help',
}

# CAPTCHA

CAPTCHA_2X_IMAGE = True
CAPTCHA_CHALLENGE_FUNCT = 'captcha.helpers.math_challenge'
CAPTCHA_IMAGE_SIZE = (120, 90)
CAPTCHA_FONT_SIZE = 30

# BLEACH

#: List of allowed tags
BLEACH_ALLOWED_TAGS = [
    'p',
    'span',
    'img',
    'div',
    'h2',
    'h5',
    'i',
    *sanitizer.ALLOWED_TAGS,
]

#: Map of allowed attributes by tag
BLEACH_ALLOWED_ATTRIBUTES = [
    'href',
    'title',
    'src',
    'alt',
    'style',
    'id',
    'class',
    'data-pswp-width',
    'data-pswp-height',
    'target',
]

BLEACH_ALLOWED_PROTOCOLS = ['ws', 'wss', *sanitizer.ALLOWED_PROTOCOLS]

BLEACH_ALLOWED_STYLES = [
    'font-family',
    'font-weight',
    'text-decoration',
    'font-variant',
    'text-align',
    'background-color',
    'max-width',
    'min-width',
    'max-height',
    'width',
    'word-break',
]

# ADMIN_SHORTCUTS

ADMIN_SHORTCUTS = [
    {
        'title': 'Shop',
        'shortcuts': [
            {
                'url_name': 'admin:shop_order_changelist',
                'title': 'Products',
                'count_new': 'project.utils.count_new_orders',
                'has_perms': 'project.utils.has_perms_to_orders',
            },
        ],
    },
]

# REDIS

REDIS_TLS_HOST = {
    'address': os.getenv('REDIS_FULL_URL'),
    'ssl_cert_reqs': None,
}
REDIS_HOSTS = ('redis', os.getenv('REDIS_PORT')) if not os.getenv('REDIS_FULL_URL') else REDIS_TLS_HOST

CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            'hosts': [REDIS_HOSTS],
        },
    },
}
