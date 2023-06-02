from flask import Flask, render_template, request, redirect
from weather_util import get_weather
from user import user_bp
from schedule import schdedule_bp
from health_bp.myhealth1_bp import health_bp1
import numpy as np
import pandas as pd

app = Flask(__name__)

app.register_blueprint(user_bp, url_prefix='/user')
app.register_blueprint(schdedule_bp, url_prefix='/schedule')
app.register_blueprint(health_bp1, url_prefix='/myhealth')

def age_gen(a) :
    age_12 = 123 - int(str(a)[:2])
    age_34 = 23 - int(str(a)[:2])
    if str(a)[-1] == '1':
        return '남성', age_12
    elif str(a)[-1] == '2':
        return '여성', age_12
    elif str(a)[-1] == '3':
        return '남성', age_34
    else:
        return '여성', age_34
    
@app.route('/')
def home():
    return render_template('home.html', weather=get_weather(app))

@app.route('/diary')
def diary():
    return render_template('diary.html', weather=get_weather(app))


if __name__ == '__main__':
    app.run(debug=True)