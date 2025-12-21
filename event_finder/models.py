from datetime import datetime
from event_finder import db, login_manager
from flask_login import UserMixin #class that comes with is_authenticated, is_anonimous, is_active and ...

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)

    def __repr__(self): #this is a magic method. This one specifically specifies how a user object should be printed out
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"
    
class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    posts = db.relationship('Post', backref='category', lazy=True)

    def __repr__(self):
        return f"Category('{self.name}')"
    
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(255), nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)    
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    event_date = db.Column(db.DateTime, nullable=False)
    duration_minutes = db.Column(db.Integer, nullable=True)
    image = db.Column(db.String(20), nullable=False, default='event_default.jpg')
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'),
                        name='fk_author',
                        nullable=False)
    category_id = db.Column(db.Integer,
                            db.ForeignKey('category.id'),
                            name='fk_post_category',
                            nullable=True)

    def __repr__(self): #this is a magic method. This one specifically specifies how a user object should be printed out
        return f"Post('{self.title}', '{self.address}', '{self.event_date}')"
