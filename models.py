from run import db


class Joke(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(120), nullable=False, unique=True)
    category = db.Column(db.String(20), nullable=False)
    likes = db.relationship('Like', backref='joke', lazy=True)

    def __repr__(self):
        return 'Joke - {}'.format(self.category)

    def getJson(self):
        joke_json = {}
        joke_json['id'] = self.id
        joke_json['content'] = self.content
        joke_json['category'] = self.category
        return joke_json


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), nullable=False, unique=True)
    likes = db.relationship('Like', backref='user', lazy=True)

    def __repr__(self):
        return 'User - {}'.format(self.username)


class Like(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    joke_id = db.Column(db.Integer, db.ForeignKey('joke.id'), nullable=False)

    def __repr__(self):
        return 'Like - {}'.format(self.id)
