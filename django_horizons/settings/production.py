from .base import *

DEBUG = False

ALLOWED_HOSTS = [".fly.dev", "localhost", "127.0.0.1"]

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

SECRET_KEY = env.str("SECRET_KEY")

try:
    from .local import *
except ImportError:
    pass
