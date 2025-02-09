# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

import multiprocessing
import os

bind = os.getenv("GUNICORN_BIND_HOST")
workers = (
    multiprocessing.cpu_count() * 2 + 1
)  # Gunicorn docs suggest this formula as the default number of workers.
accesslog = "-"
loglevel = "info"
capture_output = True
enable_stdio_inheritance = True
