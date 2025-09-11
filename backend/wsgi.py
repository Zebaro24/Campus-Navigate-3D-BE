"""
WSGI config for backend project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application
from django.db import connections
from django.db.utils import OperationalError
from time import sleep

def wait_for_db(max_attempts=8, delay=5):
    attempt = 1
    while attempt <= max_attempts:
        try:
            conn = connections['default']
            conn.cursor()
            print("✅ База доступна!")
            return
        except OperationalError:
            print(f"❌ База недоступна, попытка {attempt}/{max_attempts}")
            attempt += 1
            sleep(delay)
    print("🚫 Не удалось подключиться к базе после всех попыток")
    exit(1)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')

wait_for_db()

application = get_wsgi_application()
