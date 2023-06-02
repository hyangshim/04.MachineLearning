from flask import Flask, render_template, request, redirect
from flask import Blueprint, request, render_template, session
from flask import redirect, flash
import hashlib, base64, json
import map_util as mu
from weather_util import get_weather, get_weather_by_coord
from user import user_bp
import crawling as crawling
app = Flask(__name__)

app.secret_key = 'qwert12345'
app.config['SESSION_COOKIE_PATH'] = '/'

app.register_blueprint(user_bp,url_prefix='/user')
user_bp = Blueprint('user_bp', __name__)

@app.route('/')
def home():
    crawling_list =crawling.news()
    return render_template('home.html',weather=get_weather(app),crawling_list=crawling.news())




if __name__ == '__main__':
    app.run(debug=True)