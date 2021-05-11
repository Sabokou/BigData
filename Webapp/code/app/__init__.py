# app/__init__.py

from flask import Flask
from flask_caching import Cache

# Initialize the app
app = Flask(__name__, instance_relative_config=True)
cache = Cache(app, config={'CACHE_TYPE': 'MemcachedCache', 'CACHE_MEMCACHED_SERVERS': ':6379/0'})

# Load the config file
app.config.from_object('config')

from app import views   # Load the views
from app import legerible