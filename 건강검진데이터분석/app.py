from flask import Flask, render_template, request, redirect
from weather_util import get_weather
from user_bp.user import user_bp
from health_bp.mydisease_bp import health_bp2
from hscs_bp.body_bp import hscs_body
from hscs_bp.dspr_bp import hscs_dspr
from hscs_bp.analysis_bp import dspr_analysis
from my_util.crawling import news
from screening_bp.screening_input import screening_input
from screening_bp.screening_output import screening_output
import os
import numpy as np
import pandas as pd

app = Flask(__name__)
app.secret_key = os.urandom(24)

app.register_blueprint(user_bp, url_prefix='/user')
app.register_blueprint(health_bp2, url_prefix='/myhealth')
app.register_blueprint(screening_input, url_prefix='/screening')
app.register_blueprint(screening_output, url_prefix='/screening')
app.register_blueprint(hscs_body, url_prefix='/hscs')
app.register_blueprint(hscs_dspr, url_prefix='/hscs')
app.register_blueprint(dspr_analysis, url_prefix='/analysis')

# for AJAX ######################################################
@app.before_first_request
def before_first_request():
    global news_list
    news_list = news()

@app.route('/')
def home():
    return render_template('home.html', weather=get_weather(app), news_list = news_list)

@app.route('/home')
def home2():
    return render_template('home.html', weather=get_weather(app), news = news())

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)