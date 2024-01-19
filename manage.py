#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'learn_site.settings')
    # host = sys.argv[2] if len(sys.argv) > 2 else '0.0.0.0'
    # port = sys.argv[3] if len(sys.argv) > 3 else '8000'
    # sys.argv = [sys.argv[0], 'runserver', f'{host}:{port}']
    #sys.argv = sys.argv[:1] + sys.argv[3:]
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
