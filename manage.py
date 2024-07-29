#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
import json
from pathlib import Path

def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    
    # Load the port from db_config.json
    BASE_DIR = Path(__file__).resolve().parent
    with open(BASE_DIR / 'db_config.json') as config_file:
        config = json.load(config_file)
    
    port = config['service'].get('port', 8000)
    
    # Modify sys.argv to include the port for the runserver command
    if len(sys.argv) == 2 and sys.argv[1] == 'runserver':
        sys.argv.append(f'{port}')

    execute_from_command_line(sys.argv)

if __name__ == '__main__':
    main()
