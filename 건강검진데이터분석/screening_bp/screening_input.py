from flask import Blueprint, request, render_template, session, redirect, flash
from weather_util import get_weather
import db_sqlite.user_dao as udao
import datetime

screening_input = Blueprint('screening_input', __name__, static_folder='../static')

@screening_input.route('/input', methods=['GET', 'POST'])
def scr_input():
    if request.method == 'GET':
        return render_template('screening_input.html', weather=get_weather(screening_input))
    else:
        if request.values["uid"]:
            now = datetime.datetime.now()
            uid = request.values["uid"]
            date = int(f'{now.year}{now.month:02d}{now.day:02d}')
            weight = int(request.values["weight"]) if (request.values["weight"]) != '' else 1
            waist = int(request.values["waist"]) if (request.values["waist"]) != '' else 0
            eye_l = float(request.values["eye_left"]) if (request.values["eye_left"]) != '' else 0
            eye_R = float(request.values["eye_right"]) if (request.values["eye_right"]) != '' else 0
            bp1 = float(request.values["bp1"]) if (request.values["bp1"]) != '' else 0
            bp2 = float(request.values["bp2"]) if (request.values["bp2"]) != '' else 0
            bs = float(request.values["bs"]) if (request.values["bs"]) != '' else 0
            tg = float(request.values["tg"]) if (request.values["tg"]) != '' else 0
            hdl = float(request.values["hdl"]) if (request.values["hdl"]) != '' else 0
            ldl = float(request.values["ldl"]) if (request.values["ldl"]) != '' else 0
            hg = float(request.values["hg"]) if (request.values["hg"]) != '' else 0
            up = float(request.values["up"]) if (request.values["up"]) != '' else 0
            bc = float(request.values["bc"]) if (request.values["bc"]) != '' else 0
            ast = float(request.values["ast"]) if (request.values["ast"]) != '' else 0
            alt = float(request.values["alt"]) if (request.values["alt"]) != '' else 0
            gtp = float(request.values["gpt"]) if (request.values["gpt"]) != '' else 0

            udao.insert_disease((uid, date, weight, waist, eye_l, eye_R, bp1, bp2, bs, tg, hdl, ldl, ldl+hdl, hg, up, bc, ast, alt, gtp))
            
            flash('저장되었습니다.')
            return redirect('/')
        else :
            flash('로그인 후 이용해주세요.')
            return redirect('/')