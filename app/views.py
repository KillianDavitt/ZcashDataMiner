from flask import render_template, redirect, url_for, request, jsonify
from app import app
from tinydb import TinyDB, Query
db = TinyDB('db.json')
Transaction = Query()

@app.route('/')
def index():
    ts = db.all()    
    return jsonify(ts)
