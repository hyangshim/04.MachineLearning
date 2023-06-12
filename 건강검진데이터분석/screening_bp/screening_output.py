from flask import Blueprint, request, render_template, session, redirect, flash
from weather_util import get_weather
import db_sqlite.user_dao as udao
import datetime

screening_output = Blueprint('screening_output', __name__, static_folder='../static')

@screening_output.route('/output', methods=['GET', 'POST'])
def scr_output():
    if request.method == 'GET':
        return render_template('screening_output.html', weather=get_weather(screening_output))
    else :
        if request.values["uid"]:
            uid = request.values["uid"]
            screening_list = udao.get_disease(uid)
            return render_template('screening_output.html', scr_list = screening_list, weather=get_weather(screening_output))
        else :
            flash('로그인 후 이용해주세요.')
            return redirect('/')