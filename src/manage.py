#!/usr/bin/env python
import os
import sys

import environ

from confs import BASE_DIR


env = environ.Env()
if env.bool('DJANGO_READ_DOT_ENV_FILE', default=True):
    env.read_env(str(BASE_DIR.parent / '.env'))


if __name__ == "__main__":
    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)
