from flask import Blueprint, render_template, request,redirect,url_for
from flask_app import db
from datetime import datetime
from flask_app.models.food import Food
import os
import random
import base64

bp = Blueprint('upload', __name__)

@bp.route('/', methods=['POST', 'GET'])
def image():

    # 만약 POST 면 아래 코드 진행
    if request.method == 'POST' : 

        # 이미지 파일 request
        get_files = request.files.getlist('imgdata')
        for get_file in get_files : 
            
            # 데이터 읽기
            data = get_file.read()
            
            # 렌더링 작업
            render_file = render_picture(data)
            
            # 파싱 작업
            imgname = str(get_file).split("'")[1].split(".")[0]
            splitted = imgname.split('_')
            food_category = splitted[0]
            food_name = splitted[1]
            food_number = splitted[2]
            image_name = imgname
            
            # DB에 저장
            db.session.add(Food(
                food_name = food_name,
                food_category = food_category,
                food_number = food_number,
                image_name = image_name,
                render_file = render_file
            ))
            db.session.commit()

    # DB에 데이터가 존재하면 html에 다 넘겨주기
    # 없으면 [] 반환
    first = db.session.query(Food).first()
    if first : 
        data = db.session.query(Food).all()
    else :
        data = []

    return render_template('upload.html',data=data)

@bp.route('/delete/<image_id>', methods=['POST', 'GET'])
def upload_delete(image_id):

    # id 로 이미지 데이터 삭제
    select_image = Food.query.filter(Food.id == image_id).first()

    db.session.delete(select_image)
    db.session.commit()

    return redirect(url_for('upload.image'))

# 렌더링 함수
def render_picture(data):
    render_pic = base64.b64encode(data).decode('ascii') 
    return render_pic