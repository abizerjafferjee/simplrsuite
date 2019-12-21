from flask_app.app import app
from flask import Flask, Blueprint, render_template, abort, jsonify, request, session, make_response
import json
from datetime import datetime
from werkzeug.utils import secure_filename
import os, sys
import string
import random
import re
from flask_app.auth_decorator import token_required

# from flask_app.database.product import Product, ProductSchema
from flask_app.models import db, Product, Category, Procurement, Inventory, ProductSchema

ProductRoutes = Blueprint('ProductRoutes', __name__)

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])
def allowed_file(filename):
    """
    Return true if the filename has an extension which is allowed
    """
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def generateSKU(id, category_id, product):
    """
    Return a unique SKU based on id, category_id, product
    *This function needs a modification. This SKU is unique even when the
    product is the same. Therefore, there is no way to compare products and
    figure out whether a product has already been added using the SKU
    """
    product = product[:3].upper()
    if not re.match('^[A-Z]{3}$', product):
        product = re.sub('[^A-Z]+', random.choice(string.ascii_letters), product)
    return "{}{}00{}".format(product[:3].upper(), str(category_id), str(id))

@ProductRoutes.route('/products', methods=['POST'])
@token_required
def add(current_user):
    """
    Add a product to db
    """
    try:
        file = None
        if 'file' in request.files:
            file = request.files['file']
        
        filename = None
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            write_path = app.config['UPLOAD_FOLDER']+'/'+filename
            file.save(write_path)

        body = json.loads(request.form['body'])
        
        if not body['category']:
            raise Exception('No category selected.')

        category = Category.query.get(body['category'])
        
        try:
            product = Product(
                user = current_user.id,
                category = category,
                description = body['description'],
                code = body['code'],
                packing_type = body['packing_type'],
                packing = body['packing'],
                currency = body['currency'],
                price = float(body['price']) if body['price'] else None,
                image_path = filename,
                additional_info = body['additional_info']
            )

            db.session.add(product)
            db.session.flush()
        except:
            raise Exception('Product already exists.')

        product.sku = generateSKU(product.id, product.category_id, product.description)
        db.session.commit()

        product_schema = ProductSchema()
        output = product_schema.dump(product)

        return make_response(jsonify({'success': True, 'body': output}), 200)
    except Exception as e:
        print(e)
        return make_response(jsonify({'success': False, 'message':str(e)}), 400)

@ProductRoutes.route('/products', methods=['PUT'])
@token_required
def update_product(current_user):
    """
    Update a product in db
    *Modify to handle category updates
    """
    # fix category update
    try:
        id = request.args.get('id', type=int)
        updatedProduct = json.loads(request.data)['body']
        d = Product.query.filter_by(id=id).first()
        d.description = updatedProduct['description']
        d.packing = updatedProduct['packing']
        db.session.commit()
        return make_response(jsonify({'success': True}), 200)
    except Exception as e:
        print(e)
        return make_response(jsonify({'success': False}), 400)

@ProductRoutes.route('/products', methods=['DELETE'])
@token_required
def delete_product(current_user):
    """
    Delete a product in db by id
    """
    try:
        id = request.args.get('id', type=int)
        Product.query.filter_by(id=id).delete()
        db.session.commit()
        return make_response(jsonify({'success': True}), 200)
    except Exception as e:
        return make_response(jsonify({'success': False}), 400)

@ProductRoutes.route('/products/<int:id>', methods=['GET'])
@token_required
def get_product(current_user, id):
    """
    Get a product from db by id
    """
    try:
        product = Product.query.get(id)
        product_schema = ProductSchema()
        output = product_schema.dump(product)

        return make_response(jsonify({'success':True, 'body':output}), 200)
    except Exception as e:
        print(e)
        return make_response(jsonify({'success':False}), 400)

@ProductRoutes.route('/products', methods=['GET'])
@token_required
def get_products(current_user):
    """
    Search and paginate products for product view
    """
    try:
        page = request.args.get('page', type=int)
        per_page = 9

        products = Product.query\
            .filter(Product.user==current_user.id)\
            .paginate(page=page, per_page=per_page, error_out=False)

        product_schema = ProductSchema(many=True)
        output = product_schema.dump(products.items)
        return make_response(jsonify({'success': True, 'body': output,
                                        'page': products.page, 'prev': products.has_prev,
                                        'next': products.has_next}), 200)
    except Exception as e:
        print(e)
        return make_response(jsonify({'success': False}, 400))

@ProductRoutes.route('/products/search', methods=['GET'])
@token_required
def search_products(current_user):
    """
    Search and paginate products for product view
    """
    try:
        product = request.args.get('product', type=int)
        products = Product.query\
            .filter(Product.user==current_user.id)\
            .filter(Product.id==product)\
            .all()

        product_schema = ProductSchema(many=True)
        output = product_schema.dump(products)
        return make_response(jsonify({'success': True, 'body': output}), 200)
    except Exception as e:
        print(e)
        return make_response(jsonify({'success': False}, 400))

@ProductRoutes.route('/products/names', methods=['GET'])
@token_required
def get_names(current_user):
    """
    Return all product names from db
    """
    try:
        products = Product.query.filter(Product.user==current_user.id)
        product_names = [{'value': p.id, 'text': p.description} for p in products]
        return make_response(jsonify({'success': True, 'body': product_names}), 200)
    except Exception as e:
        return make_response(jsonify({'success': False}), 400)


