#!/bin/sh

set -e

FLASK_APP=app flask run -p 6012 --host=0.0.0.0
