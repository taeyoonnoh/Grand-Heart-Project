from flask import render_template, flash, redirect, url_for, request
from app import app, db
from app.forms import LoginForm, RegistrationForm, EditProfileForm, EmptyForm, PostForm, ResetPasswordRequestForm, ResetPasswordForm
from app.models import User, Post, Image
from werkzeug.urls import url_parse
from flask_login import current_user, login_user, logout_user, login_required
from datetime import datetime
from app.email import send_password_reset_email
import random
import re
import json


@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    user = User.verify_reset_password_token(token)
    if not user:
        return redirect(url_for('index'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash('Your password has been reset.')
        return redirect(url_for('login'))
    return render_template('reset_password.html', form=form)



@app.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            send_password_reset_email(user)
        flash('Check your email for the instructions to reset your password')
        return redirect(url_for('login'))
    return render_template('reset_password_request.html',
                           title='Reset Password', form=form)

@app.route('/follow/<username>', methods=['POST'])
@login_required
def follow(username):
    form = EmptyForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=username).first()
        if user is None:
            flash('User {} not found.'.format(username))
            return redirect(url_for('index'))
        if user == current_user:
            flash('You cannot follow yourself!')
            return redirect(url_for('user', username=username))
        current_user.follow(user)
        db.session.commit()
        flash('You are following {}!'.format(username))
        return redirect(url_for('user', username=username))
    else:
        return redirect(url_for('index'))

@app.route('/unfollow/<username>', methods=['POST'])
@login_required
def unfollow(username):
    form = EmptyForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=username).first()
        if user is None:
            flash('User {} not found.'.format(username))
            return redirect(url_for('index'))
        if user == current_user:
            flash('You cannot unfollow yourself!')
            return redirect(url_for('user', username=username))
        current_user.unfollow(user)
        db.session.commit()
        flash('You are not following {}.'.format(username))
        return redirect(url_for('user', username=username))
    else:
        return redirect(url_for('index'))

@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', title='Edit Profile',
                            form=form)



@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()

@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    page = request.args.get('page', 1, type=int)
    posts = user.posts.order_by(Post.timestamp.desc()).paginate(
        page, app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('user', username=user.username, page=posts.next_num) \
        if posts.has_next else None
    prev_url = url_for('user', username=user.username, page=posts.prev_num) \
        if posts.has_prev else None
    form = EmptyForm()
    return render_template('user.html', user=user, posts=posts.items,
                           next_url=next_url, prev_url=prev_url, form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('??? ????????? ????????? ????????? ?????? ?????? ??????????????????!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)



@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(body=form.post.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post is now live!')
        return redirect(url_for('index'))
    page = request.args.get('page', 1, type=int)
    posts = current_user.followed_posts().paginate(
        page, app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('index', page=posts.next_num) \
        if posts.has_next else None
    prev_url = url_for('index', page=posts.prev_num) \
        if posts.has_prev else None
    return render_template('index.html', title='Home', form=form,
                           posts=posts.items, next_url=next_url,
                           prev_url=prev_url)

@app.route('/explore')
@login_required
def explore():
   page = request.args.get('page', 1, type=int)
   posts = Post.query.order_by(Post.timestamp.desc()).paginate(
       page, app.config['POSTS_PER_PAGE'], False)
   next_url = url_for('explore', page=posts.next_num) \
       if posts.has_next else None
   prev_url = url_for('explore', page=posts.prev_num) \
       if posts.has_prev else None
   return render_template("index.html", title='Explore', posts=posts.items,
                         next_url=next_url, prev_url=prev_url)


from base64 import b64encode
import base64

def render_picture(data):
    render_pic = base64.b64encode(data).decode('ascii') 
    return render_pic

@app.route('/image')
def image_index():
    return render_template("upload.html")

@app.route('/upload')
@login_required
def image_upload():

    # ???????????????????????? ????????? ?????? ???????????? ???????????? ??????
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

@app.route('/upload/image', methods=['POST'])
def add_image():
    # POST??? ?????? ????????? ?????? ????????? ????????????
    
    get_files = request.files.getlist('imgdata')
    for get_file in get_files:
        data = get_file.read()
        render_file = render_picture(data)
        imgname = str(get_file).split("'")[1].split(".")[0]

        # ????????? ????????? db??? ??????
        newFile = Image(imgname=imgname, imgdata=data, rendered_data=render_file)
        db.session.add(newFile)
        db.session.commit()

    return redirect(url_for('image_upload'))

@app.route('/upload/')
@app.route('/upload/<int:image_id>')
def delete_image(image_id=None):
    
    # ????????? ????????? id??? ??????
    select_image = Image.query.filter(Image.id == image_id).first()

    # ????????? ????????? ????????? ??????X, ???????????? 400
    if image_id is None:
        return "", 400

    elif select_image is None:
        return "", 404

    else:
        # image ?????????
        db.session.delete(select_image)
        db.session.commit()
        return redirect(url_for('image_upload'))

@app.route('/random_show', methods=['GET', 'POST'])
@login_required
def random_show():

    # ???????????????????????? ????????? ?????? ???????????? ???????????? ??????
    imagedata = Image.query.all()
    image_list = []
    for image in imagedata:
        pic_date = str(image.pic_date)[0:10]
        image_dict = {'id' : image.id,
                      'imgname' : image.imgname,
                      'rendered_data' : image.rendered_data,
                      'pic_date' : pic_date}
        image_list.append(image_dict)

    # ????????? ??????
    # random_img_id = random.randint(1, len(image_list)) -1

    # filtering ????????? ???????????? ???????????? image id ??? ???????????? ?????? ??????
    current_username = current_user.username
    cat_dict = json.loads(db.session.query(User).filter(User.username==current_username).first().filter_food_json)
    cat_items_list = list(cat_dict.items())
    filtered_list = [int(key) for key,value in cat_items_list if value==0]
    random_img_id = random.choice(filtered_list)
    random_img_list = []
    random_img_list.append(image_list[random_img_id])

    # ?????????
    user = db.session.query(User).filter(User.username==current_username).first()
    
    cat_dict = json.loads(user.food_json)
    pref_dict = json.loads(user.preference_json)
    filter_dict = json.loads(user.filter_food_json)

    return render_template('random_show.html', image_list=random_img_list, data=list,current_username=current_username,cat_dict=cat_dict,pref_dict=pref_dict,filter_dict=filter_dict)

@app.route('/random_show/prefer/<random_name>', methods=['GET', 'POST'])
@login_required
def prefer(random_name):

    # {????????????}_{?????????}_{??????} ???????????? ????????????
    # ????????? ????????? ?????? 
    splitted =  random_name.split("_")
    food_category = splitted[0]
    food_name = splitted[1]

    current_username = current_user.username
    user_db = db.session.query(User).filter(User.username==current_username).first()

    # ?????? ???????????? 1??? ?????? ??? json dump
    cat_dict = json.loads(db.session.query(User).filter(User.username==current_username).first().food_json)
    cat_dict[food_category] +=1

    cat_json = json.dumps(cat_dict,ensure_ascii=False)
    user_db.food_json = cat_json

    # ?????? ????????? json ????????????
    pref_dict = json.loads(db.session.query(User).filter(User.username==current_username).first().preference_json)
    pref_dict[food_category + '_' + food_name] = 3

    pref_json = json.dumps(pref_dict,ensure_ascii=False)
    user_db.preference_json = pref_json

    # filtering ????????????
    filt_dict = json.loads(db.session.query(User).filter(User.username==current_username).first().filter_food_json)
    select_image = db.session.query(Image).filter((Image.imgname.contains(food_category + '_' + food_name))).first()
    filt_dict[str(select_image.id)] = 1
    
    filt_json = json.dumps(filt_dict,ensure_ascii=False)
    user_db.filter_food_json = filt_json

    db.session.commit()

    return redirect(url_for('random_show'))

@app.route('/random_show/soso/<random_name>', methods=['GET', 'POST'])
@login_required
def soso(random_name):

    # {????????????}_{?????????}_{??????} ???????????? ????????????
    # ????????? ????????? ?????? 
    splitted =  random_name.split("_")
    food_category = splitted[0]
    food_name = splitted[1]

    current_username = current_user.username
    user_db = db.session.query(User).filter(User.username==current_username).first()

    # ?????? ????????? json ????????????
    pref_dict = json.loads(db.session.query(User).filter(User.username==current_username).first().preference_json)
    pref_dict[food_category + '_' + food_name] = 2

    pref_json = json.dumps(pref_dict,ensure_ascii=False)
    user_db.preference_json = pref_json

    # filtering ????????????
    filt_dict = json.loads(db.session.query(User).filter(User.username==current_username).first().filter_food_json)
    select_image = db.session.query(Image).filter((Image.imgname.contains(food_category + '_' + food_name))).first()
    filt_dict[str(select_image.id)] = 1
    
    filt_json = json.dumps(filt_dict,ensure_ascii=False)
    user_db.filter_food_json = filt_json

    db.session.commit()

    return redirect(url_for('random_show'))

@app.route('/random_show/notprefer/<random_name>', methods=['GET', 'POST'])
@login_required
def notprefer(random_name):

    # {????????????}_{?????????}_{??????} ???????????? ????????????
    # ????????? ????????? ?????? 
    splitted =  random_name.split("_")
    food_category = splitted[0]
    food_name = splitted[1]

    current_username = current_user.username
    user_db = db.session.query(User).filter(User.username==current_username).first()

    # ?????? ????????? json ????????????
    pref_dict = json.loads(db.session.query(User).filter(User.username==current_username).first().preference_json)
    pref_dict[food_category + '_' + food_name] = 1

    pref_json = json.dumps(pref_dict,ensure_ascii=False)
    user_db.preference_json = pref_json

    # filtering ????????????
    filt_dict = json.loads(db.session.query(User).filter(User.username==current_username).first().filter_food_json)
    select_image = db.session.query(Image).filter((Image.imgname.contains(food_category + '_' + food_name))).first()
    filt_dict[str(select_image.id)] = 1
    
    filt_json = json.dumps(filt_dict,ensure_ascii=False)
    user_db.filter_food_json = filt_json

    db.session.commit()

    return redirect(url_for('random_show'))

# ????????? ??????
@app.route('/filter', methods=['POST', 'GET'])
@login_required
def filter():

    # DB ??? ????????? ?????? ?????? ????????? ????????? ??????
    # ????????? ???????????? ?????? ???????????? ????????? ???????????? ?????? ??????
    foods = db.session.query(Image).all()

    current_username = current_user.username
    check_if_food_json_exists = db.session.query(User.food_json).filter(User.username==current_username).first()
    check_if_filter_food_json_exists = db.session.query(User.filter_food_json).filter(User.username==current_username).first()
    check_if_preference_json_exists = db.session.query(User.preference_json).filter(User.username==current_username).first()
    if not check_if_food_json_exists[0] or not check_if_filter_food_json_exists[0] or not check_if_preference_json_exists[0]: 
        cat_dict,num_dict,pref_dict = {},{},{}
        for i in foods : 
            splitted = i.imgname.split('_')
            category = splitted[0]
            name = splitted[1]
            cat_dict[category] = 0
            num_dict[i.id] = 0
            pref_dict[category + '_' + name] = 0
        cat_json = json.dumps(cat_dict,ensure_ascii=False)
        num_json = json.dumps(num_dict,ensure_ascii=False)
        pref_json = json.dumps(pref_dict,ensure_ascii=False)
        user_db = db.session.query(User).filter(User.username==current_username).first()
        user_db.food_json = cat_json
        user_db.filter_food_json = num_json
        user_db.preference_json = pref_json
        db.session.commit()

    # ?????????
    print(db.session.query(User).filter(User.username==current_username).first().food_json)
    print(db.session.query(User).filter(User.username==current_username).first().filter_food_json)
    print(db.session.query(User).filter(User.username==current_username).first().preference_json)

    cat_dict = json.loads(db.session.query(User).filter(User.username==current_username).first().filter_food_json)
    unique_foods = set()
    for i in foods : 
        splitted = i.imgname.split('_')
        category = splitted[0]
        name = re.sub('[0-9]+','',splitted[1])
        if cat_dict[str(i.id)]==0 : 
            unique_foods.add(category+'_'+name)
    unique_foods = sorted(list(unique_foods))

    return render_template('filter.html',foods=unique_foods,cat_dict=cat_dict)

# ????????? ??? ????????? ?????? ??????
@app.route('/filter/delete', methods=['POST', 'GET'])
@login_required
def filter_delete():

    # '????????????_?????????' ????????? ?????? ??????
    # '_' ??? split ?????????
    image_cat_name = request.form['search']
    
    # ?????? ???????????? ???????????? ????????? ????????????
    if not image_cat_name : 
        return redirect(url_for('filter'))
    
    splitted = image_cat_name.split('_')
    category = splitted[0]
    name = splitted[1]

    search = category + '_' + name
    
    # filter ???????????? ?????? ????????? DB?????? ???????????????
    current_username = current_user.username
    cat_dict = json.loads(db.session.query(User).filter(User.username==current_username).first().filter_food_json)

    select_image = db.session.query(Image).filter((Image.imgname.contains(search))).all()
    for i in select_image :
        cat_dict[str(i.id)] = 1
    
    print(cat_dict)

    cat_json = json.dumps(cat_dict,ensure_ascii=False)
    user_db = db.session.query(User).filter(User.username==current_username).first()
    user_db.filter_food_json = cat_json
    db.session.commit()

    return redirect(url_for('filter'))

if __name__ == '__main__':

# debug??? True??? ????????????, ?????? ?????? ?????? ?????? ????????? ???????????? ???????????? ?????????. 
    app.run(debug = True)
