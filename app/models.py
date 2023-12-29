from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from datetime import datetime, date
from app import app, db, login_manager

@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))

@app.context_processor
def set_global_html_variable_values():
    admin_id = app.config['ADMIN_ID']
    template_config = {'admin_id': admin_id}
    return template_config

## Database Models ##
# Blog Post Model
class Posts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    content = db.Column(db.Text)
    # author = db.Column(db.String(255))
    date_posted = db.Column(db.DateTime, default=datetime.utcnow)
    slug = db.Column(db.String(255))
    # Foreign Key to link Users (primary key: user,id)
    poster_id = db.Column(db.Integer, db.ForeignKey('users.id'))


# User Model
# class Users(db.Model, UserMixin):
class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    fav_color = db.Column(db.String(120))
    about_author = db.Column(db.Text(500), nullable=True)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)
    password_hash = db.Column(db.String(128))
    # User can have many posts - need database relationship
    posts = db.relationship('Posts', backref='poster')
    profile_pic = db.Column(db.String(120), nullable=True)
    is_admin = db.Column(db.Integer, nullable=True, default=0)

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')
    
    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)


    # Create a String
    def __repr__(self):
        return '<Name %r>' % self.name