#!/bin/bash
# set -e

echo "starting server"
gunicorn --logger-class=config.logger.GunicornLogger service.wsgi:app --bind 0.0.0.0:9000 --workers=1
