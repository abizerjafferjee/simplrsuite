from flask import Flask, Blueprint, render_template, abort, jsonify, current_app,\
    request, redirect, session, make_response, url_for
import json
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash, check_password_hash
import os, sys
import jwt
from flask_app.auth_decorator import token_required

from flask_app.models import db, User, UserSchema

AuthRoutes = Blueprint('AuthRoutes', __name__)

@AuthRoutes.route('/profile', methods=["GET"])
@token_required
def profile(current_user):
    return make_response(jsonify({'success':True, 'user': current_user.to_dict()}), 200)

@AuthRoutes.route('/login', methods=["POST"])
def login():
    req = json.loads(request.data)['body']
    user = User.authenticate(**req)
    user = User.query.filter_by(email=req['email']).first()
    if not user: 
        return make_response(jsonify({'success':False, 'body':'Please check your login details and try again.'}), 401)
    
    token = jwt.encode({
        'sub': user.email,
        'iat': datetime.utcnow(),
        'exp': datetime.utcnow() + timedelta(minutes=30)
    }, current_app.config['SECRET_KEY'])

    return make_response(jsonify({'success':True, 'token': token.decode('UTF-8')}), 200)

@AuthRoutes.route('/signup', methods=["POST"])
def signup():
    req = json.loads(request.data)['body']

    user = User.query.filter_by(email=req['email']).first()

    if user:
        return make_response(jsonify({'success':False, 'body':'A user with this email already exists.'}), 200)

    new_user = User(email=req['email'], name=req['name'])
    new_user.set_password(req['password'])

    db.session.add(new_user)
    db.session.commit()

    return make_response(jsonify({'success':True}), 200)

# @AuthRoutes.route('/logout', methods=["GET"])
# def logout():
#     return make_response(jsonify({'success':True}, 200))