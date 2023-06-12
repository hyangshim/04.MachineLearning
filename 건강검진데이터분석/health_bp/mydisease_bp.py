from flask import Blueprint, request, render_template, session, redirect, flash
import numpy as np
import pandas as pd
import math, datetime
import db_sqlite.user_dao as udao
from health_bp.bp_util import su_bp5, su_bp6, su_bp7, su_bp8,su_bp9,su_bp10,su_bp11,su_bp12,su_bp13,su_bp14,su_bp15,su_bp16,su_bp17,su_bp18
from health_bp.bp_util import iw_bp5, iw_bp6, iw_bp7, iw_bp8,iw_bp9,iw_bp10,iw_bp11,iw_bp12,iw_bp13,iw_bp14,iw_bp15,iw_bp16,iw_bp17,iw_bp18
from health_bp.bp_util import gbhd5, gbhd6, gbhd7, gbhd8,gbhd9,gbhd10,gbhd11,gbhd12,gbhd13,gbhd14,gbhd15,gbhd16,gbhd17,gbhd18
from health_bp.bp_util import tgdict5, tgdict6, tgdict7, tgdict8,tgdict9,tgdict10,tgdict11,tgdict12,tgdict13,tgdict14,tgdict15,tgdict16,tgdict17,tgdict18
from health_bp.bp_util import hdldict5, hdldict6, hdldict7, hdldict8,hdldict9,hdldict10,hdldict11,hdldict12,hdldict13,hdldict14,hdldict15,hdldict16,hdldict17,hdldict18
from health_bp.bp_util import ldldict5, ldldict6, ldldict7, ldldict8,ldldict9,ldldict10,ldldict11,ldldict12,ldldict13,ldldict14,ldldict15,ldldict16,ldldict17,ldldict18
from health_bp.bp_util import ttcdict5, ttcdict6, ttcdict7, ttcdict8,ttcdict9,ttcdict10,ttcdict11,ttcdict12,ttcdict13,ttcdict14,ttcdict15,ttcdict16,ttcdict17,ttcdict18
from health_bp.bp_util import hgdict_male5, hgdict_male6, hgdict_male7, hgdict_male8,hgdict_male9,hgdict_male10,hgdict_male11,hgdict_male12,hgdict_male13,hgdict_male14,hgdict_male15,hgdict_male16,hgdict_male17,hgdict_male18
from health_bp.bp_util import hgdict_female5, hgdict_female6, hgdict_female7, hgdict_female8,hgdict_female9,hgdict_female10,hgdict_female11,hgdict_female12,hgdict_female13,hgdict_female14,hgdict_female15,hgdict_female16,hgdict_female17,hgdict_female18
from health_bp.bp_util import ydbdict5, ydbdict6, ydbdict7, ydbdict8,ydbdict9,ydbdict10,ydbdict11,ydbdict12,ydbdict13,ydbdict14,ydbdict15,ydbdict16,ydbdict17,ydbdict18
from health_bp.bp_util import ast5, ast6, ast7, ast8,ast9,ast10,ast11,ast12,ast13,ast14,ast15,ast16,ast17,ast18
from health_bp.bp_util import alt5, alt6, alt7, alt8,alt9,alt10,alt11,alt12,alt13,alt14,alt15,alt16,alt17,alt18, total
import health_bp.bp_util
from health_bp.bp_util import gtp_male5, gtp_male6, gtp_male7, gtp_male8,gtp_male9,gtp_male10,gtp_male11,gtp_male12,gtp_male13,gtp_male14,gtp_male15,gtp_male16,gtp_male17,gtp_male18
from health_bp.bp_util import gtp_female5, gtp_female6, gtp_female7, gtp_female8,gtp_female9,gtp_female10,gtp_female11,gtp_female12,gtp_female13,gtp_female14,gtp_female15,gtp_female16,gtp_female17,gtp_female18
from health_bp.bp_util import hcc5, hcc6, hcc7, hcc8,hcc9,hcc10,hcc11,hcc12,hcc13,hcc14,hcc15,hcc16,hcc17,hcc18, ast_aged, alt_aged, gtp_female_aged
from health_bp.bp_util import tg_list, hdl_list, ldl_list, tdl_list, male, female, hg_male_list, hg_female_list, ydb_abnormal, gtp_male_aged
from weather_util import get_weather

M_height = [{'신장': 145, '비율': 0.03},{'신장': 150, '비율': 0.58},{'신장': 155, '비율': 3.66},{'신장': 160, '비율': 13.2},
        {'신장': 165, '비율': 25.56},{'신장': 170, '비율': 29.86},{'신장': 175, '비율': 18.79},{'신장': 180, '비율': 6.97},
        {'신장': 185, '비율': 1.28},{'신장': 190, '비율': 0.08}]  
W_height =[{'신장': 125, '비율': 0.0},{'신장': 130, '비율': 0.02},{'신장': 135, '비율': 0.27},{'신장': 140, '비율': 2.1},
        {'신장': 145, '비율': 8.66},{'신장': 150, '비율': 22.52},{'신장': 155, '비율': 31.26},{'신장': 160, '비율': 23.97},
        {'신장': 165, '비율': 9.31},{'신장': 170, '비율': 1.77},{'신장': 175, '비율': 0.1},{'신장': 180, '비율': 0.0}]

M_height_avg=[{'나이': '20~24세', '평균키': 171.2},{'나이': '25~29세', '평균키': 171.96},{'나이': '30~34세', '평균키': 172.13},{'나이': '35~39세', '평균키': 171.99},
                {'나이': '40~44세', '평균키': 170.71},{'나이': '45~49세', '평균키': 169.46},{'나이': '50~54세', '평균키': 167.92},{'나이': '55~59세', '평균키': 166.69},{'나이': '60~64세', '평균키': 165.36},
                {'나이': '65~69세', '평균키': 163.97},{'나이': '70~74세', '평균키': 163.23},{'나이': '75~79세', '평균키': 162.23},{'나이': '80~84세', '평균키': 161.17},{'나이': '85세+', '평균키': 159.48}]
W_height_avg =[{'나이': '20~24세', '평균키': 158.98},{'나이': '25~29세', '평균키': 159.52},{'나이': '30~34세', '평균키': 159.37},
                {'나이': '35~39세', '평균키': 159.0},{'나이': '40~44세', '평균키': 157.95},{'나이': '45~49세', '평균키': 156.62},{'나이': '50~54세', '평균키': 155.17},
                {'나이': '55~59세', '평균키': 153.98},{'나이': '60~64세', '평균키': 152.7},{'나이': '65~69세', '평균키': 151.25},{'나이': '70~74세', '평균키': 150.21},{'나이': '75~79세', '평균키': 148.21},
                {'나이': '80~84세', '평균키': 146.35},{'나이': '85세+', '평균키': 144.49}]

M_weight = [{'체중': 40 , '비율': 0.1},{'체중': 45, '비율': 0.77},{'체중': 50, '비율': 2.98},{'체중': 55, '비율': 7.13},{'체중': 60, '비율': 13.17},
            {'체중': 65, '비율': 17.9},{'체중': 70, '비율': 18.84},{'체중': 75, '비율': 15.15},{'체중': 80, '비율': 10.39},{'체중': 85, '비율': 6.16},
            {'체중': 90, '비율': 3.49},{'체중': 95, '비율': 1.91},{'체중': 100, '비율': 1.02},{'체중': 105, '비율': 0.51},{'체중': 110, '비율': 0.26},{'체중': 115, '비율': 0.12},
            {'체중': 120, '비율': 0.06},{'체중': 125, '비율': 0.02},{'체중': 130, '비율': 0.01},{'체중': 135, '비율': 0.0}] 
W_weight =[{'체중': 30, '비율': 0.03},{'체중': 35, '비율': 0.46},{'체중': 40, '비율': 3.5},{'체중': 45, '비율': 12.55},{'체중': 50, '비율': 23.23},
            {'체중': 55, '비율': 23.88},{'체중': 60, '비율': 17.17},{'체중': 65, '비율': 9.75},{'체중': 70, '비율': 4.95},{'체중': 75, '비율': 2.47},
            {'체중': 80, '비율': 1.15},{'체중': 85, '비율': 0.56},{'체중': 90, '비율': 0.23},{'체중': 95, '비율': 0.1},{'체중': 100, '비율': 0.04},
            {'체중': 105, '비율': 0.01},{'체중': 110, '비율': 0.01},{'체중': 115, '비율': 0.0}]

M_weight_avg =[{'나이': '20~24세', '평균 체중': 69.82},{'나이': '25~29세', '평균 체중': 73.17},{'나이': '30~34세', '평균 체중': 75.04},{'나이': '35~39세', '평균 체중': 75.15},{'나이': '40~44세', '평균 체중': 73.53},
                {'나이': '45~49세', '평균 체중': 71.82},{'나이': '50~54세', '평균 체중': 69.86},{'나이': '55~59세', '평균 체중': 68.11},{'나이': '60~64세', '평균 체중': 66.76},{'나이': '65~69세', '평균 체중': 65.09},
                {'나이': '70~74세', '평균 체중': 64.05},{'나이': '75~79세', '평균 체중': 62.19},{'나이': '80~84세', '평균 체중': 60.15},{'나이': '85세+', '평균 체중': 57.21}]
W_weight_avg =[{'나이': '20~24세', '평균 체중': 54.43},{'나이': '25~29세', '평균 체중': 54.43},{'나이': '30~34세', '평균 체중': 55.4},{'나이': '35~39세', '평균 체중': 56.09},
                {'나이': '40~44세', '평균 체중': 56.43},{'나이': '45~49세', '평균 체중': 56.43},{'나이': '50~54세', '평균 체중': 56.32},{'나이': '55~59세', '평균 체중': 55.95},{'나이': '60~64세', '평균 체중': 56.0},
                {'나이': '65~69세', '평균 체중': 55.67},{'나이': '70~74세', '평균 체중': 55.06},{'나이': '75~79세', '평균 체중': 53.1},{'나이': '80~84세', '평균 체중': 50.84},{'나이': '85세+', '평균 체중': 46.41}]

M_BMI_avg =[{'나이': '20~24세', '평균체질량': 23.78},{'나이': '25~29세', '평균체질량': 24.7},{'나이': '30~34세', '평균체질량': 25.29},{'나이': '35~39세', '평균체질량': 25.38},{'나이': '40~44세', '평균체질량': 25.2},
            {'나이': '45~49세', '평균체질량': 24.98},{'나이': '50~54세', '평균체질량': 24.75},{'나이': '55~59세', '평균체질량': 24.49},{'나이': '60~64세', '평균체질량': 24.38},
            {'나이': '65~69세', '평균체질량': 24.18},{'나이': '70~74세', '평균체질량': 24.01},{'나이': '75~79세', '평균체질량': 23.6},{'나이': '80~84세', '평균체질량': 23.13},{'나이': '85세+', '평균체질량': 22.46}]
W_BMI_avg =[{'나이': '20~24세', '평균체질량': 21.51},{'나이': '25~29세', '평균체질량': 21.37},{'나이': '30~34세', '평균체질량': 21.8},{'나이': '35~39세', '평균체질량': 22.17},{'나이': '40~44세', '평균체질량': 22.61},
            {'나이': '45~49세', '평균체질량': 23.0},{'나이': '50~54세', '평균체질량': 23.39},{'나이': '55~59세', '평균체질량': 23.59},{'나이': '60~64세', '평균체질량': 24.01},{'나이': '65~69세', '평균체질량': 24.33},
            {'나이': '70~74세', '평균체질량': 24.39},{'나이': '75~79세', '평균체질량': 24.15},{'나이': '80~84세', '평균체질량': 23.7},{'나이': '85세+', '평균체질량': 22.2}]

M_waist=[{'허리둘레': '0-60', '비율': 0.03},{'허리둘레': '60-65', '비율': 0.32},{'허리둘레': '65-70', '비율': 1.89},{'허리둘레': '70-75', '비율': 6.61},
        {'허리둘레': '75-80', '비율': 14.72},{'허리둘레': '80-85', '비율': 24.27},{'허리둘레': '85-90', '비율': 23.67},{'허리둘레': '90-95', '비율': 15.72},{'허리둘레': '95-100', '비율': 7.79},{'허리둘레': '100이상', '비율': 4.99}]

W_waist=[{'허리둘레': '0-60', '비율': 1.02},{'허리둘레': '60-65', '비율': 6.35},{'허리둘레': '65-70', '비율': 15.04},{'허리둘레': '70-75', '비율': 20.79},
        {'허리둘레': '75-80', '비율': 20.13},{'허리둘레': '80-85', '비율': 16.86},{'허리둘레': '85-90', '비율': 10.48},
        {'허리둘레': '90-95', '비율': 5.52},{'허리둘레': '95-100', '비율': 2.41},{'허리둘레': '100이상', '비율': 1.41}]

M_waist_avg=[{'나이': '20~24세', '평균허리둘레': 80.33},{'나이': '25~29세', '평균허리둘레': 83.43},{'나이': '30~34세', '평균허리둘레': 85.49},{'나이': '35~39세', '평균허리둘레': 86.09},{'나이': '40~44세', '평균허리둘레': 85.76},
            {'나이': '45~49세', '평균허리둘레': 85.44},{'나이': '50~54세', '평균허리둘레': 85.3},{'나이': '55~59세', '평균허리둘레': 85.28},{'나이': '60~64세', '평균허리둘레': 85.64},
            {'나이': '65~69세', '평균허리둘레': 85.75},{'나이': '70~74세', '평균허리둘레': 86.03},{'나이': '75~79세', '평균허리둘레': 85.83},{'나이': '80~84세', '평균허리둘레': 85.24},{'나이': '85세+', '평균허리둘레': 83.59}]

W_waist_avg=[{'나이': '20~24세', '평균허리둘레': 70.66},{'나이': '25~29세', '평균허리둘레': 70.68},{'나이': '30~34세', '평균허리둘레': 72.36},{'나이': '35~39세', '평균허리둘레': 73.58},
            {'나이': '40~44세', '평균허리둘레': 74.77},{'나이': '45~49세', '평균허리둘레': 75.53},{'나이': '50~54세', '평균허리둘레': 76.9},{'나이': '55~59세', '평균허리둘레': 78.09},{'나이': '60~64세', '평균허리둘레': 79.84},
            {'나이': '65~69세', '평균허리둘레': 81.29},{'나이': '70~74세', '평균허리둘레': 82.32},{'나이': '75~79세', '평균허리둘레': 82.68},{'나이': '80~84세', '평균허리둘레': 82.41},{'나이': '85세+', '평균허리둘레': 79.78}]
eye_left=[{'시력_좌': '0.2미만', '비율': 1.3},{'시력_좌': '0.2-0.4', '비율': 1.24},{'시력_좌': '0.4-0.6', '비율': 2.07},{'시력_좌': '0.6-0.8', '비율': 3.11},{'시력_좌': '0.8-1.0', '비율': 5.34},
            {'시력_좌': '1.0-1.2', '비율': 5.52},{'시력_좌': '1.2-1.4', '비율': 8.58},{'시력_좌': '1.4-1.6', '비율': 10.04},{'시력_좌': '1.6-1.8', '비율': 10.71},{'시력_좌': '1.8-2.0', '비율': 20.33},{'시력_좌': '2.0이상', '비율': 0.02}]

eye_right=[{'시력_우': '0.2미만', '비율': 1.32},{'시력_우': '0.2-0.4', '비율': 1.31},{'시력_우': '0.4-0.6', '비율': 2.04},{'시력_우': '0.6-0.8', '비율': 3.16},{'시력_우': '0.8-1.0', '비율': 5.2},
            {'시력_우': '1.0-1.2', '비율': 5.44},{'시력_우': '1.2-1.4', '비율': 8.56},{'시력_우': '1.4-1.6', '비율': 10.0},{'시력_우': '1.6-1.8', '비율': 10.84},{'시력_우': '1.8-2.0', '비율': 20.74},{'시력_우': '2.0이상', '비율': 0.02}]

eye_left_avg=[{'나이': '20~24세', '평균시력': 1.09},{'나이': '25~29세', '평균시력': 1.1},{'나이': '30~34세', '평균시력': 1.12},{'나이': '35~39세', '평균시력': 1.13},{'나이': '40~44세', '평균시력': 1.11},
                {'나이': '45~49세', '평균시력': 1.05},{'나이': '50~54세', '평균시력': 1.0},{'나이': '55~59세', '평균시력': 0.95},{'나이': '60~64세', '평균시력': 0.88},{'나이': '65~69세', '평균시력': 0.81},{'나이': '70~74세', '평균시력': 0.73},{'나이': '75~79세', '평균시력': 0.66},{'나이': '80~84세', '평균시력': 0.6},{'나이': '85세+', '평균시력': 0.51}]

eye_right_avg=[{'나이': '20~24세', '평균시력': 1.08},{'나이': '25~29세', '평균시력': 1.09},{'나이': '30~34세', '평균시력': 1.11},{'나이': '35~39세', '평균시력': 1.13},
                {'나이': '40~44세', '평균시력': 1.11},{'나이': '45~49세', '평균시력': 1.05},{'나이': '50~54세', '평균시력': 1.0},{'나이': '55~59세', '평균시력': 0.95},
                {'나이': '60~64세', '평균시력': 0.88},{'나이': '65~69세', '평균시력': 0.81},{'나이': '70~74세', '평균시력': 0.74},{'나이': '75~79세', '평균시력': 0.67},{'나이': '80~84세', '평균시력': 0.61},{'나이': '85세+', '평균시력': 0.51}]
sound_left =[{'청력_좌': '정상', '비율': 96.61}, {'청력_좌': '비정상', '비율': 3.37}]
sound_right=[{'청력_우': '정상', '비율': 96.74}, {'청력_우': '비정상', '비율': 3.23}]

sound_left_avg=[{'나이': '20~24세', '비정상 청력 비율': 0.29},{'나이': '25~29세', '비정상 청력 비율': 0.18},{'나이': '30~34세', '비정상 청력 비율': 0.32},{'나이': '35~39세', '비정상 청력 비율': 0.43},{'나이': '40~44세', '비정상 청력 비율': 0.7},
                {'나이': '45~49세', '비정상 청력 비율': 1.09},{'나이': '50~54세', '비정상 청력 비율': 1.8},{'나이': '55~59세', '비정상 청력 비율': 3.04},{'나이': '60~64세', '비정상 청력 비율': 4.81},
                {'나이': '65~69세', '비정상 청력 비율': 7.3},{'나이': '70~74세', '비정상 청력 비율': 11.71},{'나이': '75~79세', '비정상 청력 비율': 16.67},{'나이': '80~84세', '비정상 청력 비율': 21.07},{'나이': '85세+', '비정상 청력 비율': 27.92}]
sound_right_avg=[{'나이': '20~24세', '비정상 청력 비율': 0.22},{'나이': '25~29세', '비정상 청력 비율': 0.2},{'나이': '30~34세', '비정상 청력 비율': 0.35},{'나이': '35~39세', '비정상 청력 비율': 0.43},{'나이': '40~44세', '비정상 청력 비율': 0.67},
                {'나이': '45~49세', '비정상 청력 비율': 1.04},{'나이': '50~54세', '비정상 청력 비율': 1.75},{'나이': '55~59세', '비정상 청력 비율': 2.94},{'나이': '60~64세', '비정상 청력 비율': 4.62},
                {'나이': '65~69세', '비정상 청력 비율': 6.97},{'나이': '70~74세', '비정상 청력 비율': 11.09},{'나이': '75~79세', '비정상 청력 비율': 15.81},{'나이': '80~84세', '비정상 청력 비율': 20.59},{'나이': '85세+', '비정상 청력 비율': 26.84}]

M_W_BMI =[{'BMI': '18.미만\n저체중', '비율': 4.42},{'BMI': '18.5-24.0\n 정상', '비율': 48.73},{'BMI': '25.0-30.0\n정상', '비율': 42.37},{'BMI': '30이상\n 비만', '비율': 4.49}]

health_bp2 = Blueprint('health_bp2', __name__, static_folder='../static')
# 연령대/성별 비율 출력 
@health_bp2.route('/disease', methods=['GET', 'POST'])
def disease():
    if request.method == 'GET':
        return render_template('my_disease.html', weather=get_weather(health_bp2))
    else:
        if request.values["uid"]:
            now = datetime.datetime.now()
            # 웹에서 입력받은 값 요청 / 사용자가 입력안할시 0으로 출력
            uid = request.values["uid"]
            user_info = udao.get_user(uid)
            date = int(f'{now.year}{now.month:02d}{now.day:02d}')
            height = float(request.values["height"]) if (request.values["height"]) != '' else 1
            weight = float(request.values["weight"]) if (request.values["weight"]) != '' else 1
            waist = float(request.values["waist"]) if (request.values["waist"]) != '' else 0
            eye_l = float(request.values["eye_left"]) if (request.values["eye_left"]) != '' else 0
            eye_R = float(request.values["eye_right"]) if (request.values["eye_right"]) != '' else 0
            sound_L = request.values["sound_L"]
            sound_R = request.values["sound_R"]
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
            gtp = float(request.values["gtp"]) if (request.values["gtp"]) != '' else 0
            smk = request.values["smoke"] if (request.values["smoke"]) != '' else 0
            drk = request.values["drink"] if (request.values["drink"]) != '' else 0

            # 입력받은 주민번호 토대로 성별/나이 판별
            gender = '남성 'if user_info[5] == 1 else '여성'
            age = health_bp.bp_util.age_cal(int(str(user_info[4])[:4]), int(str(user_info[4])[4:6]), int(str(user_info[4])[6:]))
            c_=1           # height
            d_=1           # weight
            x=1           # bmi
            MW=1          #허리둘레
            MW_E_L=1      # 시력(좌)
            MW_E_R=1      # 시력(우)
            SL=1          # 청력(좌)
            SR=1          # 청력(우)
            for age_find1, age_find2 in zip(np.arange(20, 100, 5), np.arange(24, 104, 5)):
                if age_find1 <= age <= age_find2:        #사용자 나이
                    break
            if user_info[5] == 1:
                for item_height, item_bmi,item_weight,item_waist,item_eye_left,item_eye_right,item_sound_left,item_sound_right in zip(M_height_avg, M_BMI_avg,M_weight_avg,M_waist_avg,eye_left_avg,eye_right_avg,sound_left_avg,sound_right_avg):
                    if item_height['나이'] == f"{age_find1}~{age_find2}세":
                        avg_height = item_height['평균키']
                        avg_BMI = item_bmi['평균체질량']
                        avg_weight =item_weight['평균 체중']
                        avg_waist=item_waist['평균허리둘레']
                        avg_eye_left=item_eye_left['평균시력']
                        avg_eye_right=item_eye_right['평균시력']
                        avg_sound_left=item_sound_left['비정상 청력 비율']
                        avg_sound_right=item_sound_right['비정상 청력 비율']
                        break  

                bmi = round(weight / (height / 100) ** 2, 1)
                bmi_category = ""
                if bmi < 18.5:
                    bmi_category = "저체중"
                elif bmi < 25:
                    bmi_category = "정상"
                elif bmi < 30:
                    bmi_category = "과체중"
                else:
                    bmi_category = "비만" 
            else:
                for item_height, item_bmi,item_weight,item_waist,item_eye_left,item_eye_right,item_sound_left,item_sound_right in zip(W_height_avg, W_BMI_avg,W_weight_avg,W_waist_avg,eye_left_avg,eye_right_avg,sound_left_avg,sound_right_avg):
                    if item_height['나이'] == f"{age_find1}~{age_find2}세":
                        avg_height = item_height['평균키']
                        avg_BMI = item_bmi['평균체질량']
                        avg_weight =item_weight['평균 체중']
                        avg_waist=item_waist['평균허리둘레']
                        avg_eye_left=item_eye_left['평균시력']
                        avg_eye_right=item_eye_right['평균시력']
                        avg_sound_left=item_sound_left['비정상 청력 비율']
                        avg_sound_right=item_sound_right['비정상 청력 비율']
                        break
                bmi = round(weight / (height / 100) ** 2, 1)
                bmi_category = ""
                if bmi < 18.5:
                    bmi_category = "저체중"
                elif bmi < 23:
                    bmi_category = "정상"
                elif bmi < 25:
                    bmi_category = "과체중"
                else:
                    bmi_category = "비만"

            for mm,ww in zip(np.arange(13.0,29.5,5.5),np.arange(18.5,35.0,5.5)):
                if mm <= bmi <=ww:
                    break
                else:
                    x += x
            # 키
            if user_info[5] == 2:
                waist_list=W_waist
                for a, b in zip(np.arange(120, 176, 5), np.arange(125, 181, 5)):
                    if a <= height <= b:      
                        break
                    else:
                        c_ = c_ + 1  
            else:
                waist_list=M_waist
                for i, j in zip(np.arange(140, 186, 5), np.arange(145, 191, 5)):
                    if i <= height <= j:       
                        break
                    else:
                        c_ = c_ + 1  
         
            percentile = round((1 - c_) * 100,2)
        
            
            #몸무게
            if user_info[5] == 2:
                height_list = W_height
                weight_list=W_weight
                for i, j in zip(np.arange(25, 111, 5), np.arange(30, 116, 5)):
                    if i <= weight <= j:       
                        break
                    else:
                        d_ = d_ + 1  
            else:
                height_list = M_height
                weight_list=W_weight
                for i, j in zip(np.arange(35, 131, 5), np.arange(40, 136, 5)):
                    if i <= weight <= j:      
                        break
                    else:
                        d_ = d_ + 1  
            # 허리둘레
            for i, j in zip([0 , *np.arange(60, 101, 5)], [*np.arange(60, 101, 5), 10000]):
                if i <= waist <= j:        
                    break
                else:
                    MW = MW + 1   

        # 복부비만 판별
            if user_info[5] == 1:
                if waist >= 90:
                    waist_division=(' 입니다.')
                else:
                    waist_division=('이 아닙니다.')
            else:
                if waist >= 85:
                    waist_division=(' 입니다.')
                else:
                    waist_division=('이 아닙니다.')
            # 시력(좌)
            for i, j in zip([0 , *np.arange(0.2, 2.5, 0.2)], [*np.arange(0.2, 2.5, 0.2), 10]):
                if i <= eye_l <= j:        
                    break
                else:
                    MW_E_L = MW_E_L + 1  
            # 시력(우)
            for i, j in zip([0 , *np.arange(0.2, 2.5, 0.2)], [*np.arange(0.2, 2.5, 0.2), 10]):
                if i <= eye_R <= j:        
                    break
                else:
                    MW_E_R = MW_E_R + 1  
            # 청력
            if sound_L == '좌정상':
                SL = 1
            else:
                SL = 2
            # 청력
            if sound_R == '우정상':
                SR = 1
            else:
                SR = 2
            # 사용자의 연령대에 해당하는 컬럼을 찾기 위한 판별식
            b=1
            for i, j in zip(np.arange(20, 100, 5), np.arange(24, 104, 5)):
                if i <= age <= j:
                    break
                else:
                    b = b + 1
            hgdict_male_list = [hgdict_male5, hgdict_male6, hgdict_male7, hgdict_male8,hgdict_male9,hgdict_male10,hgdict_male11,hgdict_male12,hgdict_male13,hgdict_male14,hgdict_male15,hgdict_male16,hgdict_male17,hgdict_male18][b]
            hgdict_female_list = [hgdict_female5, hgdict_female6, hgdict_female7, hgdict_female8,hgdict_female9,hgdict_female10,hgdict_female11,hgdict_female12,hgdict_female13,hgdict_female14,hgdict_female15,hgdict_female16,hgdict_female17,hgdict_female18][b]
            gtp_male_list = [gtp_male5, gtp_male6, gtp_male7, gtp_male8,gtp_male9,gtp_male10,gtp_male11,gtp_male12,gtp_male13,gtp_male14,gtp_male15,gtp_male16,gtp_male17,gtp_male18][b]
            gtp_female_list = [gtp_female5, gtp_female6, gtp_female7, gtp_female8,gtp_female9,gtp_female10,gtp_female11,gtp_female12,gtp_female13,gtp_female14,gtp_female15,gtp_female16,gtp_female17,gtp_female18][b]
            # 사용자의 혈압에 해당하는 컬럼을 찾기 위한 판별식
            sc_range1 = [0, 110, 115, 120, 125, 130, 135, 140, 145, 150]
            sc_range2 = [110, 115, 120, 125, 130, 135, 140, 145, 150, 1000]
            c=1
            for i, j in zip(sc_range1, sc_range2):
                if i <= bp1 < j:
                    break
                else:
                    c = c + 1
            iw_range1 = [0,  60,  65,  70,  75,  80,  85,  90,  95, 100]
            iw_range2 = [60,  65,  70,  75,  80,  85,  90,  95, 100, 1000]
            d=1
            for i, j in zip(iw_range1, iw_range2):
                if i <= bp2 < j:
                    break
                else:
                    d = d + 1
        
            # 고혈압 건강 연령대
            e = math.floor((c+d)/2)
            e = male[e-1]['연령']
            
            # 공복혈당 컬럼 찾기용
            bs_1 = [0,  100,  126]
            bs_2 = [100,  126,  10000]
            f=1
            for i, j in zip(bs_1, bs_2):
                if i <= bs < j:
                    break
                else:
                    f = f + 1
            
            # 공복혈당 건강 연령대
            g = male[f-1]['연령']
        
            # 트리글리세라이드 컬럼 찾기용
            h=1
            tg_1 = [0,  150,  200]
            tg_2 = [150,  200,  10000]
            for i, j in zip(tg_1, tg_2):
                if i <= tg < j:
                    break
                else:
                    h = h + 1
            
            # HDL 컬럼 찾기용
            hdlc=1
            hdl_1 = [0,  40,  60]
            hdl_2 = [40,  60,  10000]
            for m, n in zip(hdl_1, hdl_2):
                if m <= hdl < n:
                    break
                else:
                    hdlc = hdlc + 1        
            
            # LDL 컬럼 찾기용
            ldlc=1
            ldl_1 = [0,  130,  160]
            ldl_2 = [130,  160,  10000]
            for m, n in zip(ldl_1, ldl_2):
                if m <= ldl < n:
                    break
                else:
                    ldlc = ldlc + 1
            
            # 총콜레스테롤 컬럼 찾기용
            k=1
            ttc_1 = [0,  200,  240]
            ttc_2 = [200,  240,  10000]
            for m, n in zip(ttc_1, ttc_2):
                if m <= ldl+hdl < n:
                    break
                else:
                    k = k + 1
            age_list = male if gender == '남성' else female
            hgdict_list = hgdict_male_list if gender == '남성' else hgdict_female_list
            hgval = hg_male_list[b] if gender == '남성' else hg_female_list[b]
            gtpval = gtp_male_aged[b] if gender == '남성' else gtp_female_aged[b]
            gtp_list = gtp_male_list if gender == '남성' else gtp_female_list
            # 성별 갈리는거 판별용
            l=1
            if gender == '남성':
                hg_1 = [0,  13,  17.5]
                hg_2 = [13,  17.5,  10000]
                # 혈색소 컬럼찾기용
                for m, n in zip(hg_1, hg_2):
                    if m <= hg < n:
                        break
                    else:
                        l = l + 1
                # gtp 컬럼 찾기용
                q=1
                gtp_1 = [-10,  63]
                gtp_2 = [63,  10000]
                for i, j in zip(gtp_1, gtp_2):
                    if i < gtp <= j:
                        break
                    else:
                        q = q + 1
            else:
                hg_female_1 = [0,  12,  15.5]
                hg_female_2 = [12,  15.5,  10000]
                # 혈색소 컬럼찾기용
                for m, n in zip(hg_female_1, hg_female_2):
                    if m <= hg < n:
                        break
                    else:
                        l = l + 1
                # gtp 컬럼 찾기용
                q=1
                gtp_1 = [-10,  35]
                gtp_2 = [35,  10000]
                for i, j in zip(gtp_1, gtp_2):
                    if i < gtp <= j:
                        break
                    else:
                        q = q + 1 

            # 요단백 컬럼 찾기용
            m=1
            for i in range(1, 7):
                if i == up:
                    break
                else:
                    m = m + 1
            # 혈청크레아티닌 컬럼 찾기용
            n=1
            hcc_1 = [0,  12,  15.5]
            hcc_2 = [12,  15.5,  10000]
            for i, j in zip(hcc_1, hcc_2):
                if i <= bc < j:
                    break
                else:
                    n = n + 1
            # AST 컬럼 찾기용
            o=1
            ast_1 = [-10,  40]
            ast_2 = [40,  10000]
            for i, j in zip(ast_1, ast_2):
                if i < ast <= j:
                    break
                else:
                    o = o + 1
            # ALT 컬럼 찾기용
            p=1
            alt_1 = [-10,  40]
            alt_2 = [40,  10000]
            for i, j in zip(alt_1, alt_2):
                if i < alt <= j:
                    break
                else:
                    p = p + 1   

            # 연령대별 수축기/이완기혈압 비율 테이블 찾기
            subp = [su_bp5, su_bp6, su_bp7, su_bp8,su_bp9,su_bp10,su_bp11,su_bp12,su_bp13,su_bp14,su_bp15,su_bp16,su_bp17,su_bp18][b]
            iwbp = [iw_bp5, iw_bp6, iw_bp7, iw_bp8,iw_bp9,iw_bp10,iw_bp11,iw_bp12,iw_bp13,iw_bp14,iw_bp15,iw_bp16,iw_bp17,iw_bp18][b]
            gbhd = [gbhd5, gbhd6, gbhd7, gbhd8,gbhd9,gbhd10,gbhd11,gbhd12,gbhd13,gbhd14,gbhd15,gbhd16,gbhd17,gbhd18][b]
            # 연령대 평균 수축기 혈압
            scg_bp = [115, 117, 119, 120, 120, 121, 123, 124, 126, 128, 130, 131, 132,131]
            iwg_bp = [71, 72, 74, 76, 76, 77, 77, 77, 77, 77, 76, 76, 76, 75]

            #고혈압 유병자 판별
            if bp1 >= 140 or bp2 >= 90:
                gha = '이며,'
            else:
                gha = '가 아니며,'
            #당뇨병 유병자 판별
            if bs >= 126:
                dnb = '입니다.'
            else:
                dnb = '가 아닙니다.'
            # 연령대 평균수치
            tgsval, hdlval, ldlval, tdlval = tg_list[b], hdl_list[b], ldl_list[b], tdl_list[b]
            tgs_list = [tgdict5, tgdict6, tgdict7, tgdict8,tgdict9,tgdict10,tgdict11,tgdict12,tgdict13,tgdict14,tgdict15,tgdict16,tgdict17,tgdict18][b]
            hdldict_list = [hdldict5, hdldict6, hdldict7, hdldict8,hdldict9,hdldict10,hdldict11,hdldict12,hdldict13,hdldict14,hdldict15,hdldict16,hdldict17,hdldict18][b]
            ldldict_list = [ldldict5, ldldict6, ldldict7, ldldict8,ldldict9,ldldict10,ldldict11,ldldict12,ldldict13,ldldict14,ldldict15,ldldict16,ldldict17,ldldict18][b]
            ttcdict_list = [ttcdict5, ttcdict6, ttcdict7, ttcdict8,ttcdict9,ttcdict10,ttcdict11,ttcdict12,ttcdict13,ttcdict14,ttcdict15,ttcdict16,ttcdict17,ttcdict18][b]
            ydbdict_list = [ydbdict5, ydbdict6, ydbdict7, ydbdict8,ydbdict9,ydbdict10,ydbdict11,ydbdict12,ydbdict13,ydbdict14,ydbdict15,ydbdict16,ydbdict17,ydbdict18][b]
            ast_list = [ast5, ast6, ast7, ast8,ast9,ast10,ast11,ast12,ast13,ast14,ast15,ast16,ast17,ast18][b]
            alt_list = [alt5, alt6, alt7, alt8,alt9,alt10,alt11,alt12,alt13,alt14,alt15,alt16,alt17,alt18][b]
            hcc_list = [hcc5, hcc6, hcc7, hcc8,hcc9,hcc10,hcc11,hcc12,hcc13,hcc14,hcc15,hcc16,hcc17,hcc18][b]
            # 종합건강상태 점수
            r=0
            if c <=3 or d <=3:
                r+=0
            if 4 <= c <= 7 or 4 <= d <= 7:
                r+=1
            if 8 <= c or 8 <= d:
                r+=2
            if 3 <= m:
                r+=1
            else:
                r = r + (h-1) + (f-1)+ (hdlc-1) + (ldlc-1) + (k-1) + (l-1) + (n-1) + (o-1) + (p-1) + (q-1)
                
            total_list = [total]
            # 이상지질혈증 유병자 판별
            if tg >= 200 or hdl < 40 or ldl >= 160 or hdl+ldl >= 240:
                ejh = '입니다.' 
            else:
                ejh = '가 아닙니다.'

            if request.values['save']:
                udao.insert_disease((uid, date, weight, waist, eye_l, eye_R, bp1, bp2, bs, tg, hdl, ldl, ldl+hdl, hg, up, bc, ast, alt, gtp))
                flash("저장되었습니다.")
                return redirect('/myhealth/disease')
            else:
                return render_template('my_disease_res.html', age_list = age_list, age=str(age), gender=gender, b=b, scg=scg_bp[b], iwg=iwg_bp[b],
                    gha = gha, su_list = subp, iw_list = iwbp, c=c, d=d, e=e, gbhd_list=gbhd, f=f, dnb=dnb, g=g, tgsval=tgsval, hdlval=hdlval, ldlval=ldlval,
                    tdlval=tdlval, ejh=ejh, tgs_list=tgs_list, h=h, hdlc=hdlc, hdldict_list=hdldict_list,ldldict_list=ldldict_list, ldlc=ldlc,k=k, ttcdict_list=ttcdict_list,
                    hgdict_list=hgdict_list, l=l, hgval=hgval, ydbdict = ydbdict_list, m=m, ydb_abnormal = ydb_abnormal[b], hcc_list=hcc_list, n=n,
                    astval=ast_aged[b], altval=alt_aged[b], gtpval=gtpval, ast_list = ast_list, o=o, alt_list = alt_list, p=p, gtp_list = gtp_list, q=q,
                    bp1=bp1, bp2=bp2, bs=bs, tg=tg, hdl=hdl, ldl=ldl, tdl=ldl+hdl, hg=hg, up=up, bc=bc, ast=ast, alt=alt, gtp=gtp, smk=smk, drk=drk,
                    total_list = total_list, r=r,height_list=height_list, weight_list=weight_list, c_=c_,d_=d_,x=x,MW=MW,MW_E_L=MW_E_L,MW_E_R=MW_E_R,SL=SL,SR=SR,
                    avg_height=avg_height,avg_BMI=avg_BMI,avg_weight=avg_weight, bmi=bmi,bmi_category=bmi_category,percentile=percentile,bmi_list=M_W_BMI,
                    waist_list=waist_list,waist_division=waist_division,avg_waist=avg_waist,eye_left_list=eye_left,eye_right_list=eye_right,avg_eye_left=avg_eye_left,
                    avg_eye_right=avg_eye_right,sound_left_list=sound_left,sound_right_list=sound_right,avg_sound_left=avg_sound_left,avg_sound_right=avg_sound_right
                    , weather=get_weather(health_bp2))
        else:
            flash('로그인 후 이용해주세요.')
            return redirect('/')