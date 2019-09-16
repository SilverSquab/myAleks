#!/bin/bash
gunicorn --worker-class=gevent my_aleks.wsgi:application -b 127.0.0.1:8002

