from flask import render_template, redirect, url_for, request, jsonify
from app import app, db
from app.models import Transaction

@app.route('/')
def index():
    t = Transaction.query.all()
    return jsonify(t)
