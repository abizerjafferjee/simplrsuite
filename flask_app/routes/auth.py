from flask import Flask, Blueprint, render_template, abort, jsonify, request, session, make_response
from flask_login import login_user, logout_user, login_required, current_user
import json
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
import os, sys

from flask_app.app import login_manager
from flask_app.models import db, User, UserSchema

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

AuthRoutes = Blueprint('AuthRoutes', __name__)

@AuthRoutes.route('/profile', methods=["GET"])
@login_required
def profile():
    return make_response(jsonify({'success':False, 'user': current_user}, 200))

@AuthRoutes.route('/login', methods=["POST"])
def login():
    req = json.loads(request.data)['body']
    user = User.query.filter_by(email=req['email']).first()
    if not user or not check_password_hash(user.password, req['password']): 
        return make_response(jsonify({'success':False, 'body':'Please check your login details and try again.'}, 200))
         
    login_user(user, remember=req['remember'])

    return make_response(jsonify({'success':True}, 200))

@AuthRoutes.route('/signup', methods=["POST"])
def signup():
    req = json.loads(request.data)['body']

    user = User.query.filter_by(email=req['email']).first() # if this returns a user, then the email already exists in database

    if user: # if a user is found, we want to redirect back to signup page so user can try again
        return make_response(jsonify({'success':False, 'body':'A user with this email already exists.'}, 200))

    # create new user with the form data. Hash the password so plaintext version isn't saved.
    new_user = User(email=req['email'], name=req['name'], password=generate_password_hash(req['password'], method='sha256'))

    # add the new user to the database
    db.session.add(new_user)
    db.session.commit()

    return make_response(jsonify({'success':True}, 200))

@AuthRoutes.route('/logout', methods=["GET"])
@login_required
def logout():
    logout_user()
    return make_response(jsonify({'success':True}, 200))