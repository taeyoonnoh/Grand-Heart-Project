from flask import Blueprint, render_template, request
from project_app.models.images_model import Image
import random

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    return render_template('index.html')

@bp.route('/upload')
def image_index():

    # 데이터베이스에서 이미지 정보 가져오고 리스트에 저장
    imagedata = Image.query.all()
    image_list = []
    for image in imagedata:
        pic_date = str(image.pic_date)[0:10]
        image_dict = {'id' : image.id,
                      'imgname' : image.imgname,
                      'rendered_data' : image.rendered_data,
                      'pic_date' : pic_date}
        image_list.append(image_dict)

    return render_template('upload.html', image_list=image_list, data=list)

@bp.route('/random_show', methods=['GET', 'POST'])
def random_show():

    # 데이터베이스에서 이미지 정보 가져오고 리스트에 저장
    imagedata = Image.query.all()
    image_list = []
    for image in imagedata:
        pic_date = str(image.pic_date)[0:10]
        image_dict = {'id' : image.id,
                      'imgname' : image.imgname,
                      'rendered_data' : image.rendered_data,
                      'pic_date' : pic_date}
        image_list.append(image_dict)

    random_img_id = random.randint(1, len(image_list)) -1
    random_img_list = []
    random_img_list.append(image_list[random_img_id])

    return render_template('random_show.html', image_list=random_img_list, data=list)

