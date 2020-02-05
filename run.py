from flask import Flask, request, jsonify, render_template, url_for
from flask_sqlalchemy import SQLAlchemy
from random import choice

app = Flask(__name__)
app.config['SECRET_KEY'] = 'abc'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

db = SQLAlchemy(app)


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


@app.route('/')
def index():
    routes = {'/jokes': 'get all jokes', '/users': 'get all users', '/categories': 'get all categories',
              '/jokes/random': 'get a random joke', '/jokes/random?category={}': 'get a random joke of given category', '/jokes/liked_jokes?user_id={}': 'get all liked jokes of a user with user id', '/jokes/like': 'post a liked joke'}
    return render_template('index.html', routes=routes)


@app.route('/user/new', methods=['POST'])
def create_user():
    data = request.get_json()
    user = User(username=data['username'])
    db.session.add(user)
    db.session.commit()
    return jsonify({'message': 'user created'})


@app.route('/jokes')
def get_all_jokes():
    jokes = Joke.query.all()
    output = []
    for joke in jokes:
        joke_json = joke.getJson()
        output.append(joke_json)
    return jsonify(output)


@app.route('/users')
def get_all_users():
    users = User.query.all()
    output = []
    for user in users:
        user_json = {}
        user_json['id'] = user.id
        user_json['username'] = user.username
        output.append(user_json)
    return jsonify(output)


@app.route('/jokes', methods=['POST'])
def post_liked_joke():
    data = request.get_json()
    like = Like(user_id=data['user_id'], joke_id=data['joke_id'])
    db.session.add(like)
    db.session.commit()

    return jsonify({'message': 'liked joke saved'})


@app.route('/jokes', methods=['DELETE'])
def delete_liked_joke():
    user_id = request.args.get('user_id')
    joke_id = request.args.get('joke_id')
    Like.query.filter_by(user_id=user_id, joke_id=joke_id).delete()
    db.session.commit()
    return jsonify({'message': 'liked joke deleted'})


@app.route('/jokes/random')
def get_random_joke_category():
    category = request.args.get('category')

    jokes = list(Joke.query.filter_by(category=category))
    if len(jokes) != 0:
        joke = choice(jokes)
        joke_json = joke.getJson()

        return jsonify(joke_json)
    return jsonify({'message': 'no jokes in this category yet'})


@app.route('/jokes/liked_jokes')
def get_liked_jokes():
    user_id = request.args.get('user_id')
    likes = list(Like.query.filter_by(user_id=user_id))
    jokes_ids = [like.joke_id for like in likes]
    jokes = Joke.query.all()
    liked_jokes = [joke for joke in jokes if joke.id in jokes_ids]
    output = [joke.getJson() for joke in liked_jokes]
    return jsonify(output)


@app.route('/jokes/categories')
def get_categories():
    categories = ['dev', 'political', 'religion', 'animal']
    return jsonify(categories)


if __name__ == "__main__":
    app.run(debug=True)
