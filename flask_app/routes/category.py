from flask import Flask, Blueprint, render_template, abort, jsonify, request, session, make_response
import json
from datetime import datetime
from werkzeug.utils import secure_filename
import os, sys
from flask_app.auth_decorator import token_required

from flask_app.models import db, Category, CategorySchema

CategoryRoutes = Blueprint('CategoryRoutes', __name__)

@CategoryRoutes.route('/categories', methods=['GET'])
@token_required
def get(current_user):
    """
    Get all categories from db
    """
    try:
        per_page = 10
        page = request.args.get('page', type=int)
        if page:
            categories = Category.query\
                .filter(Category.user==current_user.id)\
                .paginate(page=page, per_page=per_page, error_out=False)
            category_schema = CategorySchema(many=True)
            output = category_schema.dump(categories.items)
            return make_response(jsonify({'success':True, 'categories': output,
                                        'page': categories.page, 'prev': categories.has_prev,
                                        'next': categories.has_next}), 200)  
        else:
            categories = Category.query.filter(Category.user==current_user.id)
            category_schema = CategorySchema(many=True)
            output = category_schema.dump(categories)
            return make_response(jsonify({'success':True, 'categories': output}), 200) 

    except Exception as e:
        print(e)
        return make_response(jsonify({'success': False}), 400)

@CategoryRoutes.route('/categories', methods=['POST'])
@token_required
def add(current_user):
    """
    Add category to db
    """
    try:
        body = json.loads(request.data)['body']
        new_category = Category(
            name = body,
            user = current_user.id,
            )
        db.session.add(new_category)
        db.session.commit()

        return make_response(jsonify({'success': True}), 200)

    except Exception as e:
        return make_response(jsonify({'success': False, 'message': 'Category name cannot be empty.'}), 400)

@CategoryRoutes.route('/categories', methods=['DELETE'])
@token_required
def delete(current_user):
    """
    Delete a supplier in db by id
    """
    try:
        id = request.args.get('id', type=int)
        Category.query.filter_by(id=id).delete()
        db.session.commit()
        return make_response(jsonify({'success': True}), 200)
    except Exception as e:
        return make_response(jsonify({'success': False}), 400)

@CategoryRoutes.route('/categories', methods=['PUT'])
@token_required
def update(current_user):
    """
    Handles get request for getting a supplier by id, post request for adding
    new supplier and put request for editing a supplier's information.
    """
    try:        
        id = request.args.get('id', type=int)
        req = json.loads(request.data)
        body = req['body']
        category = Category.query.get(id)

        category.name = body['name']
        db.session.commit()

        return make_response(jsonify({'success': True}), 200)

    except Exception as e:
        return make_response(jsonify({'success': False}), 400)

@CategoryRoutes.route('/categories/file', methods=['GET'])
@token_required
def add_many(current_user):
    """
    Modify this to take a file and upload to db
    """
    try:
        data = pd.read_csv('../docs/data.csv')
        data.fillna(0, inplace=True)
        data = list(data['category'].unique())

        for row in data:
            category = Category(
                name = row,
                user=current_user.id
                )
            db.session.add(category)
        db.session.commit()
        return make_response(jsonify({'success': True}), 200)
    except Exception as e:
        return make_response(jsonify({'success': False}), 400)
