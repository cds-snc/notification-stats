import os

from dotenv import load_dotenv
from flask import Flask
from flask_cors import CORS


application = Flask(__name__)
CORS(application)
