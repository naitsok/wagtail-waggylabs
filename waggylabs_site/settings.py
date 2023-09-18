"""
Django settings for Waggy Labs website project.

Generated by 'django-admin startproject' using Django 4.1.10

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
import sys


PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(PROJECT_DIR)
# sys.path.insert(0, os.path.join(BASE_DIR, "wagtail-waggylabs"))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY", default="SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = bool(int(os.environ.get("DJANGO_DEBUG", default=1)))

# Email configuration
EMAIL_BACKEND = os.environ.get("DJANGO_EMAIL_BACKEND", default="django.core.mail.backends.console.EmailBackend")
DEFAULT_FROM_EMAIL = os.environ.get("DJANGO_DEFAULT_FROM_EMAIL", default="webmaster@localhost")
EMAIL_HOST = os.environ.get("DJANGO_EMAIL_HOST", default="example.com")
EMAIL_PORT = int(os.environ.get("DJANGO_EMAIL_PORT", default=8887))
EMAIL_USE_TLS = bool(int(os.environ.get("DJANGO_EMAIL_USE_TLS", default=1)))
EMAIL_USE_SSL = bool(int(os.environ.get("DJANGO_EMAIL_USE_SSL", default=0)))
EMAIL_HOST_USER = os.environ.get("DJANGO_EMAIL_HOST_USER", default="webmaster")
EMAIL_HOST_PASSWORD = os.environ.get("DJANGO_EMAIL_HOST_PASSWORD", default="pwd")

# DJANGO_ADMINS is string consisting of name,email;name,emal;name,email...
ADMINS = os.environ.get("DJANGO_ADMINS", default=[])
if ',' in ADMINS:
    ADMINS = [(admin.split(',')[0], admin.split(',')[1]) for admin in ADMINS.split(';')]

MANAGERS = ADMINS


# SECURITY WARNING: define the correct hosts in production!
# 'DJANGO_ALLOWED_HOSTS' environment  variable should be a single string of hosts with a space between each.
# For example: 'DJANGO_ALLOWED_HOSTS=localhost 127.0.0.1 [::1]'
ALLOWED_HOSTS = os.environ.get("DJANGO_ALLOWED_HOSTS", default="*").split()
INTERNAL_IPS = os.environ.get("DJANGO_INTERNAL_IPS", default="").split()
CSRF_TRUSTED_ORIGINS = os.environ.get("DJANGO_CSRF_TRUSTED_ORIGINS", default="http://localhost:1337").split()
if os.environ.get("DJANGO_SECURE_PROXY_SSL_HEADER"):
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")



# Application definition

INSTALLED_APPS = [
    "waggylabs",
    
    "wagtail.contrib.forms",
    "wagtail.contrib.modeladmin",
    "wagtail.contrib.redirects",
    "wagtail.contrib.routable_page",
    "wagtail.contrib.settings",
    "wagtail.contrib.styleguide",
    "wagtail.contrib.table_block",
    "wagtail.embeds",
    "wagtail.sites",
    "wagtail.users",
    "wagtail.snippets",
    "wagtail.documents",
    "wagtail.images",
    "wagtail.search",
    "wagtail.admin",
    "wagtail",
    
    "modelcluster",
    "taggit",
    # "taggit_templatetags",
    "el_pagination",
    "wagtailmenus",
    "wagtailmarkdown",
    "wagtailmetadata",
    "hitcount",
    "captcha",
    
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sitemaps",
]

MIDDLEWARE = [
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "wagtail.contrib.redirects.middleware.RedirectMiddleware",
    # WaggyLabs middlewares
    "waggylabs.middleware.DjangoAdminAccessMiddleware",
]

ROOT_URLCONF = "waggylabs_site.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            os.path.join(PROJECT_DIR, "templates"),
            os.path.join(BASE_DIR, 'waggylabs', 'templates', 'waggylabs'),
        ],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "wagtail.contrib.settings.context_processors.settings",
                "wagtailmenus.context_processors.wagtailmenus",
            ],
        },
    },
]

WSGI_APPLICATION = "waggylabs_site.wsgi.application"


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": os.environ.get("DJANGO_SQL_ENGINE", "django.db.backends.sqlite3"),
        "NAME": os.environ.get("DJANGO_SQL_DATABASE", os.path.join(BASE_DIR, "db.sqlite3")),
        "USER": os.environ.get("DJANGO_SQL_USER", "user"),
        "PASSWORD": os.environ.get("DJANGO_SQL_PASSWORD", "password"),
        "HOST": os.environ.get("DJANGO_SQL_HOST", "localhost"),
        "PORT": os.environ.get("DJANGO_SQL_PORT", "5432"),
    }
}

# Set default auto field to remove warning related to somewhat older 
# Django apps where AutoField was used
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


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


# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = os.environ.get("DJANGO_TIME_ZONE", default="UTC")

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
]

STATICFILES_DIRS = [
    # os.path.join(BASE_DIR, "static"),
]

# ManifestStaticFilesStorage is recommended in production, to prevent outdated
# JavaScript / CSS assets being served from cache (e.g. after a Wagtail upgrade).
# See https://docs.djangoproject.com/en/4.1/ref/contrib/staticfiles/#manifeststaticfilesstorage
STATICFILES_STORAGE = "django.contrib.staticfiles.storage.ManifestStaticFilesStorage"

STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
STATIC_URL = "/static/"

MEDIA_ROOT = os.path.join(BASE_DIR, "mediafiles")
MEDIA_URL = "/media/"


# Wagtail settings
WAGTAIL_APPEND_SLASH = True
WAGTAIL_SITE_NAME = os.environ.get("WAGTAIL_SITE_NAME", "WaggyLabs")

# Search
# https://docs.wagtail.org/en/stable/topics/search/backends.html
WAGTAILSEARCH_BACKENDS = {
    "default": {
        "BACKEND": "wagtail.search.backends.database",
    }
}

# Base URL to use when referring to full URLs within the Wagtail admin backend -
# e.g. in notification emails. Don't include '/admin' or a trailing slash
WAGTAILADMIN_BASE_URL = os.environ.get("WAGTAILADMIN_BASE_URL", "http://example.com")
# Search backed for development
WAGTAILSEARCH_BACKENDS = {
    'default': {
        'BACKEND': 'wagtail.search.backends.database',
    }
}

# Disable password reset since it is personal site and the user is created using command line
WAGTAIL_PASSWORD_RESET_ENABLED = bool(int(os.environ.get("WAGTAIL_PASSWORD_RESET_ENABLED", default=1)))

# Passwords can be changed
WAGTAIL_PASSWORD_MANAGEMENT_ENABLED = bool(int(os.environ.get("WAGTAIL_PASSWORD_MANAGEMENT_ENABLED", default=1)))

# Users do have passwords to log in
WAGTAILUSERS_PASSWORD_ENABLED = True

# Users must have paswords
WAGTAILUSERS_PASSWORD_REQUIRED = True

# See also embeds configuration at https://docs.wagtail.org/en/stable/reference/settings.html#wagtailembeds-responsive-html
WAGTAILEMBEDS_RESPONSIVE_HTML = True

# Custom admin login form based on email
# To have default login form, comment the line
WAGTAILADMIN_USER_LOGIN_FORM = 'waggylabs.forms.CaptchaLoginForm'

# Changes whether the Submit for Moderation button is displayed in the action menu
WAGTAIL_MODERATION_ENABLED = True

# To count usage of images and documents
WAGTAIL_USAGE_COUNT_ENABLED = True

# Date and time formats for admin
# WAGTAIL_DATE_FORMAT = '%d.%m.%Y.'
# WAGTAIL_DATETIME_FORMAT = '%d.%m.%Y. %H:%M'
# WAGTAIL_TIME_FORMAT = '%H:%M'


# Wagtail menus settings
WAGTAILMENUS_ACTIVE_ANCESTOR_CLASS = "active"
WAGTAILMENUS_SECTION_ROOT_DEPTH = 3

# Wagtail markdown settings
WAGTAILMARKDOWN = {
    # ...
    "allowed_tags": ["s"],
    "extensions": [
        "waggylabs.extensions.markdown",
        ],
    "extension_configs": {
        "codehilite": {
            "linenums": True,
            }
        },
    "extensions_settings_mode": "extend",
}

# Hit Count settings
# after this time the hit from the same user will be counted again
HITCOUNT_KEEP_HIT_ACTIVE  = {"days" : 30 }
# time to keep hits in database - now the hits are stored indefinitely
# HITCOUNT_KEEP_HIT_IN_DATABASE = {'days': 30}

# El-pagination settings
EL_PAGINATION_PAGE_LIST_CALLABLE = 'el_pagination.utils.get_elastic_page_numbers' # get_page_numbers

# Taggit settings
TAGGIT_CASE_INSENSITIVE = True
TAG_SPACES_ALLOWED = True

# django-simple-captcha settings
CAPTCHA_CHALLENGE_FUNCT = 'captcha.helpers.math_challenge'
# CAPTCHA_IMAGE_SIZE = (120, 60)
CAPTCHA_FONT_SIZE = 30

# Waggy Labs settings

# Urls configuration

# WAGGYLABS_BASE_URL sets the base url for the whole WaggyLabs site
# i.e. the total url will be WAGGYLABS_BASE_URL + all other parts
# (For example, Django admin base url will be WAGGYLABS_BASE_URL +
# WAGGYLABS_DJANGO_ADMIN_BASE_URL). This is needed when a WaggyLabs
# site is added to an existing Django project.
WAGGYLABS_BASE_URL = os.environ.get("WAGGYLABS_BASE_URL", default="")
WAGGYLABS_DJANGO_ADMIN_BASE_URL = os.environ.get("WAGGYLABS_DJANGO_ADMIN_BASE_URL", default="django-admin/")
WAGGYLABS_WAGTAIL_ADMIN_BASE_URL = os.environ.get("WAGGYLABS_WAGTAIL_ADMIN_BASE_URL", default="admin/")
WAGGYLABS_WAGTAIL_DOCUMENTS_BASE_URL = os.environ.get("WAGGYLABS_WAGTAIL_DOCUMENTS_BASE_URL", default="documents/")
WAGGYLABS_CAPTCHA_BASE_URL = os.environ.get("WAGGYLABS_CAPTCHA_BASE_URL", default="simple-captcha/")
WAGGYLABS_SEARCH_URL = os.environ.get("WAGGYLABS_SEARCH_URL", default="search/")

# Navigation bar configuration
WAGGYLABS_MENU_MAX_LEVELS = 1
WAGGYLABS_MENU_ALLOW_REPEATING_PARENTS = True

# Search configuration
WAGGYLABS_SEARCH_RESULTS_PAGE_SIZE = 10

# Blocks configuration
WAGGYLABS_CARD_GRID_COLUMNS = 3
# the first element of tuple must be equal to one of the
# CodeMirror modes, e.g. python from .../python/python.min.js mode
WAGGYLABS_CODEBLOCK_LANGS =  {
    # 'CodeMirror MIME type': ('CodeMirror mode folder', 'Pygments short name', 'Human readable name')
    # https://codemirror.net/5/mode/index.html
    # https://pygments.org/languages/
    'text/x-python': ('python', 'python', 'Python'),
    'text/x-csrc': ('clike', 'c', 'C'),
    'text/x-c++src': ('clike', 'cpp', 'C++'),
    'text/x-java': ('clike', 'java', 'Java/Kotlin'),
    'text/x-csharp': ('clike', 'csharp', 'C#'),
    'text/x-objectivec': ('clike', 'objectivec', 'Objective C'),
    'text/x-scala': ('clike', 'scala', 'Scala'),
    # 'text/x-django': ('django', 'django', 'Django template markup'), # Not working
    # 'text/x-dockerfile': ('dockerfile', 'dockerfile', 'Dockerfile'),  # Not working
    'application/xml': ('xml', 'xml', 'XML'), # Needs to be before HTML mode
    'text/html': ('htmlmixed', 'html', 'HTML'),
    'text/javascript': ('javascript', 'javascript', 'Javascipt'),
    'text/json': ('javascript', 'json', 'JSON'),
    'text/typescript': ('javascript', 'typescript', 'TypeScript'),
    'text/x-mathematica': ('mathematica', 'mathematica', 'Mathematica'),
    'text/x-octave': ('octave', 'matlab', 'Matlab'),
    'application/x-powershell': ('powershell', 'powershell', 'Powershell'),
    # 'text/x-rsrc': ('r', 'r', 'R'),
    # 'text/x-rustsrc': ('rust', 'rust', 'Rust'),  # Not working
    'text/x-sh': ('shell', 'bach', 'Bach/Shell'),
    'text/x-swift': ('swift', 'swift', 'Swift'),
    'text/x-sql': ('sql', 'sql', 'SQL'),
}
WAGGYLABS_COLUMNS_MAX = 3

# Setting for upgrading to newer version of the components?
