from flask_app import db

class Food(db.Model):
    __tablename__ = 'food'

    id = db.Column(db.Integer(), primary_key = True, nullable = False)
    food_name = db.Column(db.Text())
    food_category = db.Column(db.Text())
    food_number = db.Column(db.Text())
    image_name = db.Column(db.Text())
    render_file = db.Column(db.Text())

    def __repr__(self):
        return f"food {self.id}"