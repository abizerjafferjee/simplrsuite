from flask import Flask, Blueprint, render_template, abort, jsonify, request, session, make_response
import json
from datetime import datetime
from werkzeug.utils import secure_filename
import os, sys

from flask_app.models import db, Category, CategorySchema

CategoryRoutes = Blueprint('CategoryRoutes', __name__)

@CategoryRoutes.route('/categories', methods=['GET'])
def get():
    """
    Get all categories from db
    """
    try:
        categories = Category.query.all()
        category_schema = CategorySchema(many=True)
        output = category_schema.dump(categories)
        return make_response(jsonify({'success':True, 'categories': output}, 200))    

    except Exception as e:
        print(e)
        return make_response(jsonify({'success': False}, 400))

@CategoryRoutes.route('/categories', methods=['POST'])
def add():
    """
    Add category to db
    """
    try:
        body = json.loads(request.data)['body']
        new_category = Category(name = body['name'])
        db.session.add(new_category)
        db.session.commit()
        category_schema = CategorySchema()
        output = category_schema.dump(new_category)
        return make_response(jsonify({'success': True, 'category':output}, 200))

    except Exception as e:
        print(e)
        return make_response(jsonify({'success': False}, 400))

@CategoryRoutes.route('/categories/file', methods=['GET'])
def add_many():
    """
    Modify this to take a file and upload to db
    """
    try:
        data = pd.read_csv('../docs/data.csv')
        data.fillna(0, inplace=True)
        data = list(data['category'].unique())

        for row in data:
            category = Category(name = row)
            db.session.add(category)
        db.session.commit()
        return make_response(jsonify({'success': True}, 200))
    except Exception as e:
        print(e)
        return make_response(jsonify({'success': False}, 400))
