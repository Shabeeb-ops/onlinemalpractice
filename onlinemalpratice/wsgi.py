"""
WSGI config for onlinemalpratice project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'onlinemalpratice.settings')

application = get_wsgi_application()

# Auto-run migrations on Vercel (since /tmp DB starts empty each cold start)
if os.environ.get('VERCEL'):
    try:
        from django.core.management import call_command
        call_command('migrate', '--run-syncdb', verbosity=0)
    except Exception as e:
        print(f"[WARN] Migration failed: {e}")
