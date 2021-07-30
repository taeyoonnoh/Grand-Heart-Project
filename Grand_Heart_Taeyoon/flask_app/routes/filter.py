from flask import Blueprint, render_template, request,redirect,url_for
from flask_app import db
from datetime import datetime
from flask_app.models.prefer import Prefer
from flask_app.models.food import Food
import os
import random
from wtforms import StringField, TextField, Form
from wtforms.validators import DataRequired, Length
from flask_sqlalchemy import SQLAlchemy

bp = Blueprint('filter', __name__)

@bp.route('/', methods=['POST', 'GET'])
def filter():

    # DB 에 저장된 모든 음식 이미지 데이터 찾기
    # 필터링 과정에서 어떤 음식들이 있는지 보여주기 위한 용도
    foods = db.session.query(Food).all()
    return render_template('filter.html',foods=foods)

@bp.route('/delete', methods=['POST', 'GET'])
def filter_delete():

    # '카테고리_음식명' 형태로 되어 있음
    # '_' 로 split 해주기
    image_cat_name = request.form['search']
    splitted = image_cat_name.split('_')
    category = splitted[0]
    name = splitted[1]

    # filter 메쏘드로 해당 데이터 DB에서 삭제해주기
    select_image = db.session.query(Food).filter((Food.food_category==category) & (Food.food_name==name)).first()

    db.session.delete(select_image)
    db.session.commit()

    return redirect(url_for('filter.filter'))