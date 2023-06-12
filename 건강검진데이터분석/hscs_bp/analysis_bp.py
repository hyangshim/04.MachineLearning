from flask import Blueprint, request, render_template, session, redirect, flash
from weather_util import get_weather

dspr_analysis = Blueprint('dspr_analysis', __name__, static_folder='../static')

@dspr_analysis.route('/highbp')
def barchart():
    return render_template('dspr_analysis/고혈압_변수.html', weather=get_weather(dspr_analysis))

@dspr_analysis.route('/diabetes')
def barchart_2():
    return render_template('dspr_analysis/당뇨병_변수.html', weather=get_weather(dspr_analysis))

@dspr_analysis.route('/dyslipidemia')
def barchart_10():
    return render_template('dspr_analysis/이상지질혈증_변수.html', weather=get_weather(dspr_analysis) )

@dspr_analysis.route('/anemia')
def barchart_3():
    return render_template('dspr_analysis/빈혈_변수.html', weather=get_weather(dspr_analysis))

@dspr_analysis.route('/kdndisease')
def barchart_7():
    return render_template('dspr_analysis/신장질환_변수.html', weather=get_weather(dspr_analysis))

@dspr_analysis.route('/livdisease')
def barchart_4():
    return render_template('dspr_analysis/간질환_변수.html', weather=get_weather(dspr_analysis))