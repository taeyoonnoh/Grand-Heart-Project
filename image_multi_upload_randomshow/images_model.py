from project_app import db
from datetime import datetime

class Image(db.Model):
    __tablename__ = 'image'

    id = db.Column(db.Integer, primary_key=True)
    imgname = db.Column(db.String(64), nullable=False)
    imgdata = db.Column(db.LargeBinary, nullable=False) #Actual img data
    rendered_data = db.Column(db.Text, nullable=False) # Data to render the pic in browser 
    pic_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    imgcomments = db.relationship('Comment', backref='Image', lazy=True)

    def __repr__(self):
            return f"<Image {self.id}>"