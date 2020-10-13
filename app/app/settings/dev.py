from .base import *

INSTALLED_APPS = INSTALLED_APPS + ['corsheaders',]

MIDDLEWARE += MIDDLEWARE + [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    ]

CORS_ORIGIN_ALLOW_ALL = False
CORS_ALLOW_CREDENTIALS = True
CORS_ORIGIN_WHITELIST = [
    'http://localhost:4200',
]
