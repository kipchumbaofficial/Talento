#!/usr/bin/env python3
'''Gunicorn configuration'''
import os

workers = int(os.getenv('GUNICORN_PROCESSES', '2'))
threads = int(os.getenv('GUNICORN_THREADS', '4'))
timeout = int(os.getenv('GUNICORN_TIMEOUT', '120'))
bind = os.getenv('GUNICORN_BIND', '0.0.0.0:8080')

forwarded_allow_ips = '*'
secure_scheme_headers = { 'X-Forwarded-Proto': 'https' }