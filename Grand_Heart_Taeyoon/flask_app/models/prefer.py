from flask_app import db

class Prefer(db.Model):
    __tablename__ = 'prefer'

    id = db.Column(db.Integer(), primary_key = True, nullable = False)
    food_name = db.Column(db.Text())
    food_category = db.Column(db.Text())
    image_name = db.Column(db.Text())
    time_save = db.Column(db.DateTime())
    curr_time = db.Column(db.DateTime())
    preference = db.Column(db.Integer())

    def __repr__(self):
        return f"prefer {self.id}"