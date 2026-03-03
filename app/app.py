# from models import User, Game, GameSession, Score
from flask import Flask, render_template


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login')
def login():
	return render_template('login.html')

@app.route('/register')
def register():
	return render_template('register.html')

@app.route('/pong')
def pong():
	return render_template('pong.html')

@app.route('/trexpres')
def trexpres():
	return render_template('trexpres.html')

@app.route('/atencioflash')
def atencioflash():
	return render_template('atencioflash.html')
