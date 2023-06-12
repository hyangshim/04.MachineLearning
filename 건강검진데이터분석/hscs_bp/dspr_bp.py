from flask import Blueprint, request, render_template, session, redirect, flash
from weather_util import get_weather

hscs_dspr = Blueprint('hscs_dspr', __name__, static_folder='../static')

@hscs_dspr.route('/smkrate')
def barchart():
    return render_template('hscs_dspr/흡연율.html', weather=get_weather(hscs_dspr))

@hscs_dspr.route('/drkrate')
def barchart_2():
    return render_template('hscs_dspr/음주율.html', weather=get_weather(hscs_dspr))

@hscs_dspr.route('/highbp')
def barchart_10():
    return render_template('hscs_dspr/고혈압.html', weather=get_weather(hscs_dspr))

@hscs_dspr.route('/diabetes')
def barchart_3():
    return render_template('hscs_dspr/당뇨병.html', weather=get_weather(hscs_dspr))

@hscs_dspr.route('/dyslipidemia')
def barchart_7():
    return render_template('hscs_dspr/이상지질혈증.html', weather=get_weather(hscs_dspr))

@hscs_dspr.route('/anemia')
def barchart_4():
    return render_template('hscs_dspr/빈혈.html', weather=get_weather(hscs_dspr))

@hscs_dspr.route('/kdndisease')
def barchart_5():
    return render_template('hscs_dspr/신장.html', weather=get_weather(hscs_dspr))

@hscs_dspr.route('/livdisease')
def barchart_6():
    return render_template('hscs_dspr/간.html', weather=get_weather(hscs_dspr))