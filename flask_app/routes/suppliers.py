from flask import Flask, Blueprint, render_template, abort, jsonify, request, session, make_response
import json
from datetime import datetime
from werkzeug.utils import secure_filename
import os, sys

from flask_app.models import db, Supplier, SupplierSchema

SupplierRoutes = Blueprint('SupplierRoutes', __name__)

@SupplierRoutes.route('/suppliers/<int:id>', methods=['GET'])
def get(id):
    """
    Handles get request for getting a supplier by id, post request for adding
    new supplier and put request for editing a supplier's information.
    """
    try:
        # id = request.args.get('id', type=int)
        supplier = Supplier.query.get(id)
        supplier_schema = SupplierSchema()
        output = supplier_schema.dump(supplier)
        return make_response(jsonify({'success': True, 'body': output}, 200))

    except Exception as e:
        print(e)
        return make_response(jsonify({'success': False}, 400))

@SupplierRoutes.route('/suppliers', methods=['POST'])
def add():
    """
    Handles post request for adding new supplier.
    """
    try:
        req = json.loads(request.data)
        body = req['body']
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
        return make_response(jsonify({'success': False}, 400))

@SupplierRoutes.route('/suppliers', methods=['PUT'])
def update():
    """
    Handles get request for getting a supplier by id, post request for adding
    new supplier and put request for editing a supplier's information.
    """
    try:        
        id = request.args.get('id', type=int)
        req = json.loads(request.data)
        body = req['body']
        supplier = Supplier.query.get(id)

        supplier.business_name = body['business_name'],
        supplier.contact_person = body['contact_person'],
        supplier.email = body['email'],
        supplier.phone = body['phone'],
        supplier.plus_code = body['plus_code'],
        supplier.address = body['address'],
        supplier.additional_info = body['additional_info']
        db.session.commit()

        supplier_schema = SupplierSchema()
        output = supplier_schema.dump(supplier)
        return make_response(jsonify({'success': True, 'body': output}, 200))

    except Exception as e:
        print(e)
        return make_response(jsonify({'success': False}, 400))

@SupplierRoutes.route('/suppliers', methods=['DELETE'])
def delete():
    """
    Delete a supplier in db by id
    """
    try:
        id = request.args.get('id', type=int)
        print(id)
        Supplier.query.filter_by(id=id).delete()
        db.session.commit()
        return make_response(jsonify({'success': True}, 200))
    except Exception as e:
        print(e)
        return make_response(jsonify({'success': False}, 400))

@SupplierRoutes.route('/suppliers', methods=['GET'])
def search():
    try:
        per_page = 6
        page = request.args.get('page', type=int)
        search = request.args.get('search', type=str)

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
    except Exception as e:
        print(e)
        return make_response(jsonify({'success': False}, 400))

@SupplierRoutes.route('/suppliers/names', methods=['GET'])
def get_names():
    try:
        suppliers = Supplier.query.all()
        supplier_names = [{'value': s.id, 'text': s.business_name} for s in suppliers]
        return make_response(jsonify({'success': True, 'suppliers': supplier_names}, 200))
    except:
        return make_response(jsonify({'success': False}, 400))
