from flask_app import db

class Good(db.Model):
    __tablename__ = 'good'

    id = db.Column(db.Integer(), primary_key = True, nullable = False)
    food_name = db.Column(db.Text())
    food_category = db.Column(db.Text())
    food_address = db.Column(db.Text())
    time_save = db.Column(db.DateTime())
    curr_time = db.Column(db.DateTime())

    def __repr__(self):
        return f"Good {self.id}"