from flask import Blueprint, render_template, request,redirect,url_for
from flask_app import db
from datetime import datetime
from flask_app.models.prefer import Prefer
from flask_app.models.food import Food
import os
import random

bp = Blueprint('main', __name__)

@bp.route('/', methods=['POST', 'GET'])
def index():

    # 랜덤으로 하나 추출하는 코드
    rand = random.randrange(0, db.session.query(Food).count()) 
    random_food = db.session.query(Food)[rand]

    # 현재 시간
    curr_time = datetime.now()

    # 우선 선호, 비선호 데이터베이스에 데이터가 있느지부터 확인
    # 없으면 [] 넣어주기
    prefer_first = db.session.query(Prefer).first()

    if prefer_first : 
        prefer_data = db.session.query(Prefer).all()
    else :
        prefer_data = []
    
    # 현재 시간 - 이미지 저장되었을 때 시간 
    # 그 차이가 300초 (5분) 이상이면 delete
    if prefer_data : 
        for i in prefer_data : 
            i.curr_time = curr_time
            if i.curr_time.timestamp() - i.time_save.timestamp() >=300 : 
                db.session.delete(i)
    db.session.commit()

    return render_template('main.html',prefer_data=prefer_data,random_food=random_food)

# 선호 
@bp.route('/prefer/<random_name>', methods=['POST', 'GET'])
def prefer(random_name):

    # {카테고리}_{음식명}_{번호} 형식으로 되어있음
    # 필요한 부분만 추출 
    splitted =  random_name.split("_")
    food_category = splitted[0]
    food_name = splitted[1]

    # 저장시간 및 현재시간 담기
    save_time = datetime.now()
    curr_time = save_time
    db.session.add(Prefer(
        food_name = food_name,
        food_category = food_category,
        time_save = save_time,
        curr_time = curr_time,
        preference = 1
    ))
    db.session.commit()
    return redirect(url_for('main.index'))

# 비선호 
@bp.route('/not_prefer/<random_name>', methods=['POST', 'GET'])
def not_prefer(random_name):

    # {카테고리}_{음식명}_{번호} 형식으로 되어있음
    # 필요한 부분만 추출 
    splitted =  random_name.split("_")
    food_category = splitted[0]
    food_name = splitted[1]

    # 저장시간 및 현재시간 담기
    save_time = datetime.now()
    curr_time = save_time
    db.session.add(Prefer(
        food_name = food_name,
        food_category = food_category,
        time_save = save_time,
        curr_time = curr_time,
        preference = 0
    ))
    db.session.commit()
    return redirect(url_for('main.index'))
