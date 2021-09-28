from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / "subdir".
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-xc1tr-g7xq!*q23t_=wq9+ij_+@oax!2gr9m-vy1u5zz8$dp01"

# SECURITY WARNING: don"t run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["*"]


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    "django_summernote",

    "app",
    "language"
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "main.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "templates")],
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

WSGI_APPLICATION = "main.wsgi.application"

AUTH_USER_MODEL = "app.User"

# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

# if DEBUG:
#     DATABASES = {
#         "default": {
#             "ENGINE": "django.db.backends.sqlite3",
#             "NAME": BASE_DIR / "db.sqlite3",
#         }
#     }
# else:
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "hamidulloh",
        "USER": "postgres",
        "PASSWORD": "hamidulloh",
        "HOST": "127.0.0.1",
        "PORT": "5432",
    }
}

# DATABASES = {
#     "default": {
#         "ENGINE": "django.db.backends.postgresql",
#         "NAME": "d4rtjf7s8c92io",
#         "HOST": "ec2-34-195-143-54.compute-1.amazonaws.com",
#         "USER": "xfvonuqiynkprn",
#         "PORT": 5432,
#         "PASSWORD": "545e3e37c9051282ba70ed84168dc927e1eef236afe50a2e0d792f5596e78d2a"
#     }
# }

# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "Asia/Tashkent"

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "static")
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "staticfiles")
]

MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


BOT_TOKEN = "1718813659:AAH6BASTk49RE3e5gpQhfcVTQLR8k4pNVGU"


SUMMERNOTE_CONFIG = {
    "iframe": True,

    # You can put custom Summernote settings
    "summernote": {
        # As an example, using Summernote Air-mode
        "airMode": False,

        # Change editor size
        "width": "100%",
        "height": "480",

        # Use proper language setting automatically (default)
        "lang": None,

        # Toolbar customization
        # https://summernote.org/deep-dive/#custom-toolbar-popover
        "toolbar": [
            ["font", ["bold", "underline", "clear"]],
            ["para", ["ul", "ol"]],
            ["insert", ["link"]],
            ["view", ["fullscreen"]],
        ],
        "codemirror": {
            "mode": "htmlmixed",
            "lineNumbers": "true",
            # You have to include theme file in "css" or "css_for_inplace" before using it.
            "theme": "monokai",
        },
    },
    # Codemirror as codeview
    # If any codemirror settings are defined, it will include codemirror files automatically.
    "css": (
        "//cdnjs.cloudflare.com/ajax/libs/codemirror/5.29.0/theme/monokai.min.css",
    ),

    # Lazy initialization
    # If you want to initialize summernote at the bottom of page, set this as True
    # and call `initSummernote()` on your page.
    "lazy": True
}

X_FRAME_OPTIONS = "SAMEORIGIN"