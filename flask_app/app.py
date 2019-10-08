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
from werkzeug.utils import secure_filename

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
# helpers
#############################################################
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])
def allowed_file(filename):  
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

#############################################################
# manage products
#############################################################
@app.route('/products/add', methods=['POST'])
def add_product():
    try:
        file = None
        if 'file' in request.files:
            file = request.files['file']
        
        filepath = None
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)

        body = json.loads(request.form['body'])

        category = Category.query.filter_by(name=body['category']).first()
        product = Product(
            category = category,
            description = body['description'],
            code = body['code'],
            packing = body['packing'],
            price = float(body['price']),
            image_path = filepath
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

@app.route('/products', methods=['POST'])
def get_products():
    try:
        # page = request.args.get('page', type=int)
        per_page = 24

        resp = json.loads(request.data)
        page = resp['page']
        search = resp['search']
        category = resp['category']

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
    except:
        return make_response(jsonify({'success': False}, 400))

@app.route('/products/names', methods=['GET'])
def get_product_names():
    try:
        products = Product.query.all()
        product_names = [{'value': p.id, 'text': p.description} for p in products]
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

###############################################################
# manage suppliers
###############################################################
@app.route('/suppliers/add', methods=['POST'])
def add_suppliers():

    try:
        req = json.loads(request.data)
        body = req['body']
        if 'supplier' in req:
            # edit supplier
            id = req['supplier']
            supplier = Supplier.query.get(id)
            for key in body:
                supplier[key] = body[key]
            db.session.commit()
            print(supplier)
        else:
            supplier = Supplier(
                business_name = body['business_name'],
                contact_person = body['contact_person'],
                email = body['email'],
                phone = body['phone'],
                plus_code = body['plus_code'],
                address = body['address'],
                additional_info = body['additional_info']
            )
            
            db.session.add(supplier)
            db.session.commit()

        supplier_schema = SupplierSchema()
        output = supplier_schema.dump(supplier)

        return make_response(jsonify({'success': True, 'body': output}, 200))
    except Exception as e:
        print(e)
        return make_response(jsonify({'success': False, 'error': 'Unable to get data. Please make sure input is valid.'}, 400))

@app.route('/suppliers', methods=['POST'])
def get_suppliers():
    try:
        # page = request.args.get('page', type=int)
        per_page = 6

        resp = json.loads(request.data)
        page = resp['page']
        search = resp['search']

        if search != '':
            print("searching")
            suppliers = Supplier.query.filter(Supplier.business_name.like(search)).paginate(page=page, per_page=per_page, error_out=False)
        else:
            suppliers = Supplier.query.paginate(page=page, per_page=per_page, error_out=False)

        supplier_schema = SupplierSchema(many=True)
        output = supplier_schema.dump(suppliers.items)
        return make_response(jsonify({'success': True, 'body': output,
                                        'page': suppliers.page, 'prev': suppliers.has_prev,
                                        'next': suppliers.has_next}, 200))
    except:
        return make_response(jsonify({'success': False}, 400))

@app.route('/suppliers/get', methods=['GET'])
def get_supplier():
    try:
        supplier_id = request.args.get('id', type=int)
        supplier = Supplier.query.get(supplier_id)
        supplier_schema = SupplierSchema()
        output = supplier_schema.dump(supplier)
        return make_response(jsonify({'success': True, 'body': output}, 200))
    except:
        return make_response(jsonify({'success': False}, 400))

@app.route('/suppliers/names', methods=['GET'])
def get_supplier_names():
    try:
        suppliers = Supplier.query.all()
        supplier_names = [{'value': s.id, 'text': s.business_name} for s in suppliers]
        return make_response(jsonify({'success': True, 'suppliers': supplier_names}, 200))
    except:
        return make_response(jsonify({'success': False}, 400))

###############################################################
# manage inventory and procurement
###############################################################
@app.route('/inventory/add', methods=['POST'])
def update_inventory():
    try:
        body = json.loads(request.data)['body']
        supplier = Supplier.query.filter_by(id=body['supplier']).first()
        product = Product.query.filter_by(id=body['product']).first()
        quantity = body['quantity']
        unit_cost = body['unit_cost']
        total_cost = body['total_cost']
        invoice = body['invoice']
        additional_info = body['additional_info']

        inventory = Inventory.query.filter_by(product_id = body['product']).first()

        if inventory:
            inventory.quantity += quantity
            db.session.commit()
        else:
            inventory = Inventory(
                product = product,
                quantity = quantity
            )
            db.session.add(inventory)
            db.session.commit()

        procurement = Procurement(
            product = product,
            supplier = supplier,
            quantity = quantity,
            unit_cost = unit_cost,
            total_cost = total_cost,
            invoice = invoice,
            additional_info = additional_info
        )

        db.session.add(procurement)
        db.session.commit()

        return make_response(jsonify({'success': True}, 200))
    except Exception as e:
        print(e)
        return make_response(jsonify({'success': False}, 400))
        

port = os.getenv('PORT', '5000')
if __name__ == "__main__":
    app.run(debug=False, host='localhost', port=int(port), threaded=True)