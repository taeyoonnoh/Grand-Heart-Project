from flask import Blueprint, render_template, request,redirect,url_for
from flask_app import db
from datetime import datetime
from flask_app.models.model import Image

bp = Blueprint('main', __name__)

@bp.route('/', methods=['POST', 'GET'])
def index():

    curr_time = datetime.now()

    if request.method=='POST' : 
        image_url = 'C:\\Users\\taeyo\\OneDrive\\바탕 화면\\project\\Grand_Heart_Taeyoon\\Data\\KFoods\\Foods\\구이_갈비구이1_0002.jpg'
        splitted =  image_url.split("\\")[-1].replace('.jpg','').split("_")
        food_category = splitted[0]
        food_name = splitted[1]

        save_time = datetime.now()
        db.session.add(Image(
            food_name = food_name,
            food_category = food_category,
            food_address = image_url,
            time_save = save_time,
            curr_time = curr_time,
        ))
        db.session.commit()
        return redirect(url_for('main.index'))
    
    first = db.session.query(Image).first()
    if not first : 
        return render_template('main.html',first=[])
    
    first.curr_time = curr_time
    db.session.commit()

    if first.curr_time.timestamp() - first.time_save.timestamp() >=300 : 
        delete = db.session.query(Image).first()
        db.session.delete(delete)
        db.session.commit()
        return render_template('main.html',first=[])

    return render_template('main.html',first=first)
    
    