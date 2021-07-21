from flask import Blueprint, render_template, request,redirect,url_for
from flask_app import db
from datetime import datetime
from flask_app.models.good import Good
from flask_app.models.bad import Bad
import os
import random

bp = Blueprint('main', __name__)

@bp.route('/', methods=['POST', 'GET'])
def index():

    # 음식 이미지가 담긴 로컬 주소값
    paths = 'C:\\Users\\taeyo\\OneDrive\\바탕 화면\\project\\Grand_Heart_Taeyoon\\flask_app\\static\\image\\KFoods\\Foods'
    
    # static 하위 폴더
    image_path = 'image/KFoods/Foods/'
    
    # 음식 이미지 파일명이 담긴 리스트 반환
    food_images_list = os.listdir(paths)
    
    # 이 중 랜덤으로 하나 선택
    selected_name = random.choice(food_images_list)
    
    # url_for 형식에 맞게 주소값 변환
    path = image_path+selected_name
    image_file = url_for('static',filename=path)

    # 현재 시간
    curr_time = datetime.now()

    # 우선 선호, 비선호 데이터베이스에 데이터가 있느지부터 확인
    # 없으면 [] 넣어주기
    good_first = db.session.query(Good).first()
    bad_first = db.session.query(Bad).first()

    if good_first : 
        good_data = db.session.query(Good).all()
    else :
        good_data = []
    
    if bad_first : 
        bad_data = db.session.query(Bad).all()
    else :
        bad_data = []
    
    # 현재 시간 - 이미지 저장되었을 때 시간 
    # 그 차이가 300초 (5분) 이상이면 delete
    if good_data : 
        for i in good_data : 
            i.curr_time = curr_time
            if i.curr_time.timestamp() - i.time_save.timestamp() >=300 : 
                db.session.delete(i)

    # 현재 시간 - 이미지 저장되었을 때 시간 
    # 그 차이가 300초 (5분) 이상이면 delete
    if bad_data : 
        for i in bad_data : 
            i.curr_time = curr_time
            if i.curr_time.timestamp() - i.time_save.timestamp() >=300 : 
                db.session.delete(i)
    db.session.commit()

    return render_template('main.html',good_data=good_data,bad_data=bad_data,image_file=image_file,selected_name = selected_name)

# 선호 데이터베이스
@bp.route('/good', methods=['POST', 'GET'])
def good():

    # 음식명 요청
    selected_name = request.form['selected_name']

    # {카테고리}_{음식명}_{번호}.jpg 형식으로 되어있음
    # 필요한 부분만 추출 
    splitted =  selected_name.replace('.jpg','').split("_")
    food_category = splitted[0]
    food_name = splitted[1]

    # 음식 데이터 주소값 담기
    paths = 'C:\\Users\\taeyo\\OneDrive\\바탕 화면\\project\\Grand_Heart_Taeyoon\\flask_app\\static\\image\\KFoods\\Foods'
    food_address = paths + '\\' + selected_name

    # 저장시간 및 현재시간 담기
    save_time = datetime.now()
    curr_time = save_time
    db.session.add(Good(
        food_name = food_name,
        food_category = food_category,
        food_address = food_address,
        time_save = save_time,
        curr_time = curr_time,
    ))
    db.session.commit()
    return redirect(url_for('main.index'))

# 비선호 데이터베이스
@bp.route('/bad', methods=['POST', 'GET'])
def bad():

    # 음식명 요청
    selected_name = request.form['selected_name']

    # {카테고리}_{음식명}_{번호}.jpg 형식으로 되어있음
    # 필요한 부분만 추출 
    splitted =  selected_name.replace('.jpg','').split("_")
    food_category = splitted[0]
    food_name = splitted[1]

    # 음식 데이터 주소값 담기
    paths = 'C:\\Users\\taeyo\\OneDrive\\바탕 화면\\project\\Grand_Heart_Taeyoon\\flask_app\\static\\image\\KFoods\\Foods'
    food_address = paths + '\\' + selected_name

    # 저장시간 및 현재시간 담기
    save_time = datetime.now()
    curr_time = save_time
    db.session.add(Bad(
        food_name = food_name,
        food_category = food_category,
        food_address = food_address,
        time_save = save_time,
        curr_time = curr_time,
    ))
    db.session.commit()
    return redirect(url_for('main.index'))