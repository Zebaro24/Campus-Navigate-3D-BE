#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys

from time import sleep
from django.db import connections
from django.db.utils import OperationalError


MAX_ATTEMPTS = 8
DELAY_SECONDS = 5

def wait_for_db():
    attempt = 1
    while attempt <= MAX_ATTEMPTS:
        try:
            db_conn = connections['default']
            db_conn.cursor()
            print("✅ БД доступна!")
            return
        except OperationalError:
            print(f"❌ Немає підключення до БД. Спроба {attempt}/{MAX_ATTEMPTS}")
            attempt += 1
            sleep(DELAY_SECONDS)
    print("🚫 Не вдалося під'єднатися до БД після усіх спроб")
    exit(1)

def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    wait_for_db()
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
