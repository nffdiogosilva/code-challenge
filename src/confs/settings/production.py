from .base import *


DEBUG = False

TEMPLATE_DEBUG = DEBUG

# Allow all host headers
ALLOWED_HOSTS = ['*']

INSTALLED_APPS += (
)


## 3rd Party settings ##

# Sentry
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

sentry_sdk.init(
    dsn=env('SENTRY_DSN'),
    integrations=[DjangoIntegration()],
    # If you wish to associate users to errors (assuming you are using
    # django.contrib.auth) you may enable sending PII data.
    send_default_pii=True,
)
