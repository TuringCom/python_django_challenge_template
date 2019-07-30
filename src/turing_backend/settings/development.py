from .base import *

DEBUG = True

STRIPE_API_KEY = "sk_test_lomdOfxbm7QDgZWvR82UhV6D"

# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'turing',
        'USER': 'root',
        'PASSWORD': 'root',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}

SOCIAL_AUTH_FACEBOOK_KEY = '860025437682601'
SOCIAL_AUTH_FACEBOOK_SECRET = 'c9e546a49cfe53c030faf43adb83765c'
