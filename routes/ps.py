from flask import Blueprint, render_template, request, redirect, url_for
from database import * 
from forms import OTCForm

routingPS = Blueprint('ps', __name__)

@routingPS.route('/')
def index():
    ps_list = PlanSalidaLibertad.select()
    return render_template('ps/index.html', ps_list=ps_list)



