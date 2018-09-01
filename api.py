from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy

import datetime
import uuid
import jwt

from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

app.config['SECRET_KEY'] = '1234'
app.config['SQLALCHEMY_DATABASE_URI'] = r'sqlite:///database.db'

db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(50), unique=True)
    name = db.Column(db.String(50))
    password = db.Column(db.String(80))
    admin = db.Column(db.Boolean)


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(50))
    complete = db.Column(db.Boolean)
    user_id = db.Column(db.Integer)


@app.route('/')
def slash():
    return 'Pong'


@app.route('/<something>')
def home(something):
    return f' This is {something}'


@app.route('/user', methods=['GET'])
def get_all_users():

    users = User.query.all()

    user_list = [dict(public_id=user.public_id, name=user.name,
                      password=user.password, admin_bool=user.admin) for user in users]

    return jsonify({'Users': user_list})


@app.route('/user/<public_id>', methods=['GET', 'POST'])
def get_one_user(public_id):
    data = request.get_json()

    user = User.query.filter_by(public_id=public_id).first()

    if not user:
        return jsonify({'Error': 'No user found!'})

    if data['key'] == 123:
        user_list = dict(id=user.id, public_id=user.public_id, name=user.name, password=user.password, admin_bool=user.admin)
        return jsonify({'user': user_list})

    user_list = dict(public_id=user.public_id, name=user.name, password=user.password, admin_bool=user.admin)

    return jsonify({'User': user_list})


@app.route('/user', methods=['POST'])
def create_user():
    data = request.get_json()
    if 'name' not in data.keys() or 'password' not in data.keys():
        return jsonify({'You have to use this model:': '{"user": "username", "password": "chosenpassword"}'})

    hashed_password = generate_password_hash(data['password'], method='sha256')
    new_user = User(public_id=str(uuid.uuid4()), name=data['name'], password=hashed_password, admin=False)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'New user created!'})


@app.route('/user/<public_id>', methods=['PUT'])
def promote_user(public_id):
    user = User.query.filter_by(public_id=public_id).first()

    if not user:
        return jsonify({'Error': 'No user found!'})
    user.admin = True
    db.session.commit()

    return jsonify({'Success 200': f'User {user.name} is now an admin'})


@app.route('/user/<public_id>', methods=['DELETE'])
def delete_user(public_id):

    user = User.query.filter_by(public_id=public_id).first()
    if not user:
        return

    store_name = user.name
    db.session.delete(user)
    db.session.commit()

    return f'User {store_name} has been deleted'


@app.route('/login')
def login():
    auth = request.authorization

    if not auth or not auth.username or not auth.username:
        return make_response('Could not verify', 401, {'WWW-Authenticate': 'Basic realm="Login required"!'})

    user = User.query.filter_by(name=auth.username).first()

    if not user:
        return make_response('User not found', 401, {'WWW-Authenticate': 'Basic realm="Login required"!'})

    if check_password_hash(user.password, auth.password):

        token = jwt.encode({'public_id': user.public_id, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, key=app.config['SECRET_KEY'])

        return jsonify({'token': token.decode('UTF-8')})

    return make_response('Password incorrect', 401, {'WWW-Authenticate': 'Basic realm="Login required"!'})


if __name__ == '__main__':
    app.run(debug=True)
