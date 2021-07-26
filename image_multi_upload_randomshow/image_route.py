from project_app import db
from project_app.models.images_model import Image
from flask import Blueprint, render_template, request, redirect, url_for, Response
from base64 import b64encode
import base64

bp = Blueprint('image', __name__)

def render_picture(data):
    render_pic = base64.b64encode(data).decode('ascii') 
    return render_pic

@bp.route('/')
def image_index():
    return render_template("upload.html")

@bp.route('/upload', methods=['POST'])
def add_image():
    # POST일 경우 이미지 파일 데이터 가져오기
    
    get_files = request.files.getlist('imgdata')
    for get_file in get_files:
        data = get_file.read()
        render_file = render_picture(data)
        imgname = str(get_file).split("'")[1].split(".")[0]

        # 이미지 데이터 db에 저장
        newFile = Image(imgname=imgname, imgdata=data, rendered_data=render_file)
        db.session.add(newFile)
        db.session.commit()
    # breakpoint()

    return redirect(url_for('main.image_index', msg_code=0))

@bp.route('/upload/')
@bp.route('/upload/<int:image_id>')
def delete_image(image_id=None):
    
    # 삭제할 이미지 id로 선택
    select_image = Image.query.filter(Image.id == image_id).first()

    # 이미지 아이디 없으면 리턴X, 상태코드 400
    if image_id is None:
        return "", 400

    elif select_image is None:
        return "", 404

    else:

        # image 지우기
        db.session.delete(select_image)
        db.session.commit()
        return redirect(url_for('main.image_index', msg_code=3))
