from flask_app.app import app
from flask import Flask, Blueprint, render_template, abort, jsonify, request, session, make_response
import json
from datetime import datetime
from werkzeug.utils import secure_filename
import os, sys
import string
import random
import re

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
def add():
    """
    Add a product to db
    """
    try:
        file = None
        if 'file' in request.files:
            file = request.files['file']
        
        filepath = None
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            # filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            filepath = app.config['UPLOAD_FOLDER']+'/'+filename
            file.save(filepath)

        body = json.loads(request.form['body'])

        category = Category.query.filter_by(name=body['category']).first()
        product = Product(
            category = category,
            description = body['description'],
            product_type = body['product_type'],
            code = body['code'],
            packing_type = body['packing_type'],
            packing = body['packing'],
            currency = body['currency'],
            price = float(body['price']) if body['price'] else None,
            image_path = filepath
        )

        db.session.add(product)
        db.session.flush()
        product.sku = generateSKU(product.id, product.category_id, product.description)
        db.session.commit()

        product_schema = ProductSchema()
        output = product_schema.dump(product)

        return make_response(jsonify({'success': True, 'body': output}, 200))
    except Exception as e:
        print(e)
        return make_response(jsonify({'success': False}, 400))

@ProductRoutes.route('/products', methods=['PUT'])
def put():
    """
    Update a product in db
    *Modify to handle category updates
    """
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
    except Exception as e:
        print(e)
        return make_response(jsonify({'success': False}, 400))

@ProductRoutes.route('/products', methods=['DELETE'])
def delete():
    """
    Delete a product in db by id
    """
    try:
        id = request.args.get('id', type=int)
        print(id)
        Product.query.filter_by(id=id).delete()
        db.session.commit()
        return make_response(jsonify({'success': True}, 200))
    except Exception as e:
        print(e)
        return make_response(jsonify({'success': False}, 400))

@ProductRoutes.route('/products/<int:id>', methods=['GET'])
def get(id):
    """
    Get a product from db by id
    """
    try:
        product = Product.query.get(id)
        product_schema = ProductSchema()
        output = product_schema.dump(product)
        return make_response(jsonify({'success':True, 'body':output}, 200))
    except Exception as e:
        print(e)
        return make_response(jsonify({'success':False}, 400))

@ProductRoutes.route('/products', methods=['GET'])
def search():
    """
    Search and paginate products for product view
    """
    try:
        page = request.args.get('page', type=int)
        search = request.args.get('search', type=str)
        category = request.args.get('category', type=str)

        per_page = 24

        if search != '' and category != '':
            print("searching text and category")
            products = Product.query.filter(Product.description.like(search)).join(Category).filter(Category.name == category).paginate(page=page, per_page=per_page, error_out=False)
        elif category != '':
            print("searching category")
            products = Product.query.join(Category).filter(Category.name == category).paginate(page=page, per_page=per_page, error_out=False)
        elif search != '':
            print("searching")
            products = Product.query.filter(Product.description.like(search)).paginate(page=page, per_page=per_page, error_out=False)
        else:
            products = Product.query.paginate(page=page, per_page=per_page, error_out=False)

        product_schema = ProductSchema(many=True)
        output = product_schema.dump(products.items)
        return make_response(jsonify({'success': True, 'body': output,
                                        'page': products.page, 'prev': products.has_prev,
                                        'next': products.has_next}, 200))
    except Exception as e:
        print(e)
        return make_response(jsonify({'success': False}, 400))

@ProductRoutes.route('/products/names', methods=['GET'])
def get_names():
    """
    Return all product names from db
    """
    try:
        products = Product.query.all()
        product_names = [{'value': p.id, 'text': p.description, 'packing_type': p.packing_type} for p in products]
        return make_response(jsonify({'success': True, 'products': product_names}, 200))
    except Exception as e:
        print(e)
        return make_response(jsonify({'success': False}, 400))

@ProductRoutes.route('/products/file', methods=['GET'])
def add_many():
    """
    Modify this function to take a multipart form of a file with many products
    and add to db
    """
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


