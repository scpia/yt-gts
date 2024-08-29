from flask import Flask
from flask_caching import Cache
from googleapiclient.discovery import build
from config import APP_KEY, YOUTUBE_API_KEY, youtube_client_conn
import sqlite3, logging


logging.basicConfig(level=logging.DEBUG)
app = Flask(__name__)
cache = Cache(app, config={'CACHE_TYPE': 'simple'})
cache.init_app(app)
app.secret_key = APP_KEY


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"
