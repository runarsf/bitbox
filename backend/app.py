#!/usr/bin/env python3
import os
import logging
from werkzeug.exceptions import HTTPException
from flask import Flask, abort, request, jsonify, g, url_for
from flask_httpauth import HTTPBasicAuth
from passlib.apps import custom_app_context as pwd_context
from itsdangerous import (TimedJSONWebSignatureSerializer
                          as Serializer, BadSignature, SignatureExpired)

from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

#DB_FILE = os.environ.get('DB_FILE', 'db.sqlite')
DB_URL = os.environ.get('DB_URL', 'sqlite:///db.sqlite')
PORT = os.environ.get('DB_PORT', 5000)

logging.basicConfig(stream=sys.stdout,
                    #filename='gp.log',
                    level=logging.DEBUG,
                    format='[%(asctime)s] [%(levelname)s] %(name)s %(message)s',
                    datefmt='%d/%m/%Y %H:%M:%S'
                    )
log = logging.getLogger(__name__)

# initialization
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'supersecretkey')

engine = create_engine(DB_URL)
Session = sessionmaker(bind=engine)
Base = declarative_base()

# extensions
auth = HTTPBasicAuth()

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    #username = Column(String(32), unique=True, nullable=False, index=True)
    email = Column(String(80), unique=True, nullable=True, index=True)
    password_hash = Column(String(64))
    uploads = relationship('Upload', backref='user', lazy=True)

    #def __init__(self, id, username, email, password_hash, categories):

    def __repr__(self):
        return "<User(username='%s')>" % (self.username)

    def hash_password(self, password):
        self.password_hash = pwd_context.hash(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password_hash)

    def generate_auth_token(self, expiration=600):
        s = Serializer(app.config['SECRET_KEY'], expires_in=expiration)
        return s.dumps({'id': self.id})

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None    # valid token, but expired
        except BadSignature:
            return None    # invalid token
        user = User.query.get(data['id'])
        return user

class Upload(Base):
    __tablename__ = 'uploads'

    # TODO: Make id a random string.
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=True)

    def __repr__(self):
        return "<Upload(id='%s', user_id='%s')>" % (self.id, self.content, self.user_id)

@auth.verify_password
def verify_password(username_or_token, password):
    # first try to authenticate by token
    user = User.verify_auth_token(username_or_token)
    if not user:
        # try to authenticate with username/password
        user = session.query(User).filter_by(username=username_or_token).first()
        if not user or not user.verify_password(password):
            return False
    g.user = user
    return True


@app.route('/api/register', methods=['POST'])
def _api_register():
    """
    curl -i -X POST -H "Content-Type: application/json" -d '{"username":"unnamde","password":"pword"}' http://127.0.0.1:5000/api/register
    """
    username = request.json.get('username')
    password = request.json.get('password')
    if username is None or password is None:
        abort(400, description='Missing arguments.')
    # TODO: Check if this is necessary, since unique=True is set.
    if session.query(User).filter_by(username=username).first() is not None:
        abort(403, description='A user with that username already exists.')
    user = User(username=username)
    user.hash_password(password)
    try:
        session.add(user)
        session.commit()
    except:
        session.rollback()
    return jsonify({
        'success': True,
        'username': user.username
    }), 201, {
        'Location': f'/api/user/{user.id}'
    }

@app.route('/api/category', methods=['POST'])
@auth.login_required
def _api_category():
    """
    curl -u unnamde:pword -i -X POST -H "Content-Type: application/json" -d '{"title":"TestCategory"}' http://127.0.0.1:5000/api/category
    """
    category_title = request.json.get('title')
    if category_title is None:
        abort(400, description='Missing arguments.')
    category = Category(title=category_title, user_id=g.user.id)
    try:
        session.add(category)
        session.commit()
    except Exception as err:
        session.rollback()
        raise Exception(err)
    return jsonify({
        'success': True,
        'username': category.title
    }), 201

@app.route('/api/email', methods=['POST'])
@auth.login_required
def _api_email():
    """
    curl -u unnamde:pword -i -X POST -H "Content-Type: application/json" -d '{"new_email":"root@runarsf.dev"}' http://127.0.0.1:5000/api/email
    """
    new_email = request.json.get('new_email')
    # TODO: Check if session.commit() is required after this.
    g.user.email = new_email
    return jsonify({
        'success': True,
        'message': 'Email changed.'
    }), 200

@app.route('/api/password', methods=['POST'])
@auth.login_required
def _api_password():
    """
    curl -u unnamde:pword -i -X POST -H "Content-Type: application/json" -d '{"new_password":"pword"}' http://127.0.0.1:5000/api/password
    """
    new_password = request.json.get('new_password')
    g.user.hash_password(new_password)
    return jsonify({
        'success': True,
        'message': 'Password changed.'
    }), 200

@app.route('/api/delete', methods=['DELETE', 'POST'])
@auth.login_required
def _api_delete():
    """
    curl -u unnamde:pword -i -X POST http://127.0.0.1:5000/api/delete
    """
    # FIXME: Should this method be converted into a method of the User class?
    try:
        session.query(User).filter_by(id=g.user.id).delete()
        session.commit()
    except Exception as err:
        session.rollback()
        raise Exception(err)
    return jsonify({
        'success': True,
        'message': 'User deleted.'
    }), 200

@app.route('/api/user/<int:uid>', methods=['GET'])
def _api_user_id(uid):
    """
    curl -i -X GET http://127.0.0.1:5000/api/user/1
    """
    #user = User.query.get(uid)
    user = session.query(User).filter_by(id=uid).first()
    if not user:
        abort(404, description='User not found.')
    return jsonify({
        'success': True,
        'username': user.username
    }), 200

@app.route('/api/token', methods=['GET'])
@auth.login_required
def _api_token():
    """
    curl -u unnamde:pword -i -X GET http://127.0.0.1:5000/api/token
         -u <token>:token
    """
    _tokenDurationHours = 600
    # TODO: Is this actually committed to the database?
    token = g.user.generate_auth_token(_tokenDurationHours)
    return jsonify({
        'success': True,
        'token': token.decode('ascii'),
        'duration': _tokenDurationHours
    }), 200

@app.route('/api/profile', methods=['GET'])
@auth.login_required
def _api_profile():
    """
    curl -u unnamde:pword -i -X GET http://127.0.0.1:5000/api/profile
    """
    return jsonify({
        'success': True,
        'username': g.user.username,
        'email': g.user.email,
        'password_hash': g.user.password_hash
    }), 200


@app.errorhandler(Exception)
def handle_error(err):
    code = 500
    if isinstance(err, HTTPException):
        code = err.code
    return jsonify({
        'success': False,
        'error': str(err)
    }), code


if __name__ == '__main__':
    session = Session()
    Base.metadata.create_all(engine)

    app.run(host='0.0.0.0', port=PORT, debug=True)
