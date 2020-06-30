import os

try:
    from . import BASE_DIR
    import environ
    env = environ.Env()
    env.read_env(str(BASE_DIR / '.env'))
except ImportError:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'confs.settings.production')

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
