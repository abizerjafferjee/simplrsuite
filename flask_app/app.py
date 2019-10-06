import os, sys
from flask import Flask, jsonify, request, render_template, make_response
import config
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_cors import CORS
import json
import pandas as pd
from numpy import genfromtxt
from flask_marshmallow import Marshmallow

app = Flask(__name__)
app.config.from_object(config.Config)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
ma = Marshmallow(app)

# enable CORS
# CORS(app, resources={r'/*': {'origins': '*'}})
cors = CORS(app)

from models import *

#############################################################
# manage products
#############################################################
@app.route('/products/add', methods=['POST'])
def add_product():
    body = json.loads(request.data)['body']
    try:
        category = Category.query.filter_by(name=body['category']).first()
        product = Product(
            category = category,
            description = body['description'],
            code = body['code'],
            packing = body['packing'],
            price = float(body['price'])
        )
        
        db.session.add(product)
        db.session.commit()

        product_schema = ProductSchema()
        output = product_schema.dump(product)
        return make_response(jsonify({'success': True, 'body': output}, 200))
    except Exception as e:
        print(e)
        return make_response(jsonify({'success': False, 'error': 'Unable to get data. Please make sure input is valid.'}, 400))

@app.route('/products/add/many', methods=['GET'])
def add_products():
    try:
        data = pd.read_csv('../docs/data.csv')
        data.fillna(0, inplace=True)
        data = data.to_json(orient='records')
        data = json.loads(data)

        for row in data:
            category = Category.query.filter_by(name = row['category']).first()

            product = Product(
                category = category,
                description = row['description'],
                code = row['code'],
                packing = row['packing'],
                price = float(row['setlife_price'])
            )

            inventory = Inventory(
                product = product,
                quantity = float(row['quantity'])
            )

            procurement = Procurement(
                product = product,
                unit_cost = float(row['price']),
                quantity = float(row['quantity']),
                total_cost = float(row['cost'])
            )

            db.session.add(product)
        db.session.commit()
        return make_response(jsonify({'success': True}, 200))
    except Exception as e:
        print(e)
        return make_response(jsonify({'success': False}, 400))

@app.route('/products', methods=['GET'])
def get_products():
    page = request.args.get('page', type=int)
    per_page = 21
    product = Product.query.paginate(page,per_page,error_out=False)
    print(type(product))
    product_schema = ProductSchema(many=True)
    output = product_schema.dump(product)
    return make_response(jsonify({'success': True, 'body': output}, 200))

@app.route('/products/names', methods=['GET'])
def get_product_names():
    try:
        products = Product.query.all()
        product_names = [{'value': p.id, 'text': p.description} for p in products]
        # product_schema = ProductSchema(many=True)
        # output = product_schema.dump(product)
        return make_response(jsonify({'success': True, 'products': product_names}, 200))
    except:
        return make_response(jsonify({'success': False}, 400))

@app.route('/products/edit', methods=['PUT'])
def put_product():
    # fix category update
    try:
        id = request.args.get('id', type=int)
        updatedProduct = json.loads(request.data)['product']
        d = Product.query.filter_by(id=id).first()
        for key, val in updatedProduct.items():
            # if key == 'category':
                # category = Category.query.filter_by(name = row['category']).first()
            setattr(d, key, val)
        db.session.commit()
        return make_response(jsonify({'success': True}, 200))
    except:
        return make_response(jsonify({'success': False}, 400))

@app.route('/products/delete', methods=['DELETE'])
def delete_product():
    try:
        id = request.args.get('id', type=int)
        print(id)
        Product.query.filter_by(id=id).delete()
        db.session.commit()
        return make_response(jsonify({'success': True}, 200))
    except:
        return make_response(jsonify({'success': False}, 400))

###############################################################
# manage categories
###############################################################

@app.route('/categories', methods=['GET'])
def get_categories():
    try:
        categories = Category.query.all()
        category_schema = CategorySchema(many=True)
        output = category_schema.dump(categories)
        return make_response(jsonify({'success':True, 'categories': output}, 200))    
    except Exception as e:
        print(e)
        return make_response(jsonify({'success':False}, 400))

@app.route('/categories/add', methods=['POST'])
def add_category():
        try:
            body = json.loads(request.data)['body']
            new_category = Category(
                name = body['name']
            )
            db.session.add(new_category)
            db.session.commit()
            category_schema = CategorySchema()
            output = category_schema.dump(new_category)
            return make_response(jsonify({'success': True, 'category':output}, 200))
        except Exception as e:
            print(e)
            return make_response(jsonify({'success': False, 'error': 'Unable to get data. Please make sure input is valid.'}, 400))

@app.route('/categories/add/many', methods=['GET'])
def add_categories():
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

###############################################################
# manage mailing list
###############################################################
@app.route('/mailer/add', methods=['POST'])
def add_mailer():
        try:
            body = json.loads(request.data)['body']
            new_mailer = MailList(
                name = body['name'],
                business = body['business'],
                email = body['email'],
                phone = body['phone'],
                remark = body['remark']
            )
            db.session.add(new_mailer)
            db.session.commit()
            mail_schema = MailListSchema()
            output = mail_schema.dump(new_mailer)
            return make_response(jsonify({'success': True, 'mailer':output}, 200))
        except Exception as e:
            print(e)
            return make_response(jsonify({'success': False, 'error': 'Unable to get data. Please make sure input is valid.'}, 400))

port = os.getenv('PORT', '5000')
if __name__ == "__main__":
    app.run(debug=False, host='localhost', port=int(port), threaded=True)