# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

import os

bind = os.getenv('GUNICORN_BIND_HOST')
workers = int(os.getenv('WORKERS'))  # only integers
accesslog = '-'
loglevel = 'info'
capture_output = True
enable_stdio_inheritance = True
