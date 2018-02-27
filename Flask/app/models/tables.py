from app import db
from datetime import date

class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(40), unique=True)
    password = db.Column(db.String(40))
    admin = db.Column(db.Boolean)

    @property
    def is_authenticated(self):
        return True
    @property
    def is_active(self):
        return True
    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)

    def get_name(self):
        return str(self.username)

    def __init__(self, username, password, admin):
        self.username = username
        self.password = password
        self.admin = admin

    def __repr__(self):
        return "<User %r>" % self.username


class Post(db.Model):
    __tablename__ = "posts"
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.Text)
    sub_category = db.Column(db.Text)
    content = db.Column(db.Text)
    user_id = db.Column(db.String(40), db.ForeignKey('users.username'), nullable=False)
    status = db.Column(db.Integer, nullable=False)
    pub_date = db.Column(db.Date, nullable=False, default=date.today)

    user = db.relationship('User', backref=db.backref('users', lazy=True))

    def __init__(self, category, sub_category, content, user_id, status):
        self.category = category
        self.sub_category = sub_category
        self.content = content
        self.user_id = user_id
        self.status = status

    def __repr__(self):
        return "%r" % self.id
