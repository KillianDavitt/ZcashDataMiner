import os
from flask import Flask, request, redirect,url_for
from config import basedir

app = Flask(__name__, static_url_path='/static')
app.config.from_object('config')

from app import views

