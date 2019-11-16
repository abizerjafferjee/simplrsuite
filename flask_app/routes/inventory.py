from flask import Flask, Blueprint, render_template, abort, jsonify, request, session, make_response
import json
from datetime import datetime
from werkzeug.utils import secure_filename
import os, sys
from flask_app.auth_decorator import token_required

from flask_app.models import db, Inventory, Procurement, Supplier, Product, InventorySchema, ProcurementSchema

InventoryRoutes = Blueprint('InventoryRoutes', __name__)

@InventoryRoutes.route('/inventory', methods=['POST'])
@token_required
def add_inventory(current_user):
    try:
        body = json.loads(request.data)['body']
        supplier = Supplier.query.filter_by(id=body['supplier']).first()
        product = Product.query.filter_by(id=body['product']).first()
        quantity = float(body['quantity'])
        unit_cost = float(body['unit_cost'])
        total_cost = float(body['total_cost'])
        currency = body['currency']
        paid = body['paid']
        invoice = body['invoice']
        location = body['location']
        additional_info = body['additional_info']

        inventory = Inventory.query\
            .filter(Inventory.user==current_user.id)\
            .filter_by(product_id = body['product']).first()

        if inventory:
            inventory.quantity += quantity
            db.session.commit()
        else:
            inventory = Inventory(
                user = current_user.id,
                product = product,
                quantity = quantity
            )
            db.session.add(inventory)

        procurement = Procurement(
            user = current_user.id,
            product = product,
            supplier = supplier,
            quantity = quantity,
            currency = currency,
            unit_cost = unit_cost,
            total_cost = total_cost,
            paid = paid,
            invoice = invoice,
            location = location,
            additional_info = additional_info
        )

        db.session.add(procurement)
        db.session.commit()

        return make_response(jsonify({'success': True}, 200))
    except Exception as e:
        print(e)
        return make_response(jsonify({'success': False}, 400))

@InventoryRoutes.route('/inventory/<int:id>', methods=['GET'])
@token_required
def get_inventory(current_user, id):
    """
    Get inventory from db by id
    """
    try:
        inventory = Inventory.query.get(id)
        schema = InventorySchema()
        output = schema.dump(inventory)
        
        return make_response(jsonify({'success':True, 'body':output}, 200))
    except Exception as e:
        print(e)
        return make_response(jsonify({'success':False}, 400))

@InventoryRoutes.route('/inventory', methods=['PUT'])
@token_required
def edit_inventory(current_user):
    try:
        id = request.args.get('id', type=int)
        updatedInventory = json.loads(request.data)['body']
        d = Inventory.query.get(id)
        d.quantity = float(updatedInventory['quantity'])
        db.session.commit()
        return make_response(jsonify({'success': True}, 200))
    except Exception as e:
        return make_response(jsonify({'success': False}, 400))

@InventoryRoutes.route('/inventory/<int:id>', methods=['DELETE'])
@token_required
def delete_inventory(current_user, id):
    try:
        inventory = Inventory.query\
            .filter(Inventory.user==current_user.id)\
            .filter_by(product_id = id).delete()
        db.session.commit()
        return make_response(jsonify({'success': True}, 200))
    except Exception as e:
        return make_response(jsonify({'success': False}, 400))


#######################################################
# Procurements
#######################################################
@InventoryRoutes.route('/procurement', methods=['GET'])
@token_required
def get_procurement(current_user):
    """
    get the 10 latest procurement records
    """
    try:
        page = request.args.get('page', type=int)
        per_page = 10
        procurements = Procurement.query\
            .filter(Procurement.user==current_user.id)\
            .order_by(Procurement.id.desc())\
            .paginate(page=page, per_page=per_page, error_out=False)
        procurement_schema = ProcurementSchema(many=True)
        output = procurement_schema.dump(procurements.items)
        return make_response(jsonify({'success': True, 'body':output, 'page': procurements.page,
                                      'prev': procurements.has_prev,
                                      'next': procurements.has_next}, 200))
    except Exception as e:
        print(e)
        returnmake_response(jsonify({'success': False}, 400))

@InventoryRoutes.route('/procurement/product/<int:id>', methods=['GET'])
@token_required
def get_procurement_by_product(current_user, id):
    """
    Get procurement from db by product id
    """
    try:
        page = request.args.get('page', type=int)
        per_page = 3
        inventory = Procurement.query\
            .filter(Procurement.user==current_user.id)\
            .filter(Procurement.product_id == id)\
            .order_by(Procurement.created.desc())\
            .paginate(page=page, per_page=per_page, error_out=False)
        schema = ProcurementSchema(many=True)
        output = schema.dump(inventory.items)
        
        return make_response(jsonify({'success':True, 'body':output, 'page': inventory.page,
                                      'prev': inventory.has_prev,
                                      'next': inventory.has_next}, 200))
    except Exception as e:
        print(e)
        return make_response(jsonify({'success':False}, 400))

@InventoryRoutes.route('/procurement/supplier/<int:id>', methods=['GET'])
@token_required
def get_procurement_by_supplier(current_user, id):
    """
    Get procurement from db by supplier id
    """
    try:
        page = request.args.get('page', type=int)
        per_page = 10
        inventory = Procurement.query\
            .filter(Procurement.user==current_user.id)\
            .filter(Procurement.supplier_id == id)\
            .order_by(Procurement.created.desc())\
            .paginate(page=page, per_page=per_page, error_out=False)
        schema = ProcurementSchema(many=True)
        output = schema.dump(inventory.items)
        
        return make_response(jsonify({'success':True, 'body':output,
                                      'page': inventory.page,
                                      'prev': inventory.has_prev,
                                      'next': inventory.has_next}, 200))
    except Exception as e:
        print(e)
        return make_response(jsonify({'success':False}, 400))

@InventoryRoutes.route('/procurement', methods=['PUT'])
@token_required
def edit_procurement(current_user):
    """
    edit a procurement record from the 10 latest procurement records
    update the inventory model as well, if the inventory quantity has changed
    """
    try:
        id = request.args.get('id', type=int)
        procurement = Procurement.query.get(id)

        req = json.loads(request.data)
        body = req['body']
        product = body['product']['id']
        invoice = body['invoice']
        quantity = float(body['quantity'])
        unit_cost = float(body['unit_cost'])
        total_cost = float(body['total_cost'])

        # print(procurement.quantity, quantity)

        # update quantity in both inventory and procurement if it has changed
        if procurement.quantity - quantity != 0:
            inventory_record = Inventory.query\
                .filter(Inventory.user==current_user.id)\
                .filter_by(product_id = product).first()
            inventory_record.quantity = inventory_record.quantity - procurement.quantity + quantity
            procurement.quantity = quantity
        
        procurement.invoice = invoice
        procurement.unit_cost = unit_cost
        procurement.total_cost = total_cost

        db.session.commit()

        return make_response(jsonify({'success': True}, 200))
    except Exception as e:
        return make_response(jsonify({'success': False}, 400))

@InventoryRoutes.route('/procurement', methods=['DELETE'])
@token_required
def delete_procurement(current_user):
    """
    Delete a procurement record in db by id
    subtract the procurement quantity from inventory
    """
    try:
        id = request.args.get('id', type=int)
        procurement = Procurement.query.filter_by(id=id)
        procurement_record = procurement.first()
        inventory = Inventory.query.filter_by(product_id = procurement_record.product_id).first()
        inventory.quantity = inventory.quantity - procurement_record.quantity
        procurement.delete()
        db.session.commit()
        return make_response(jsonify({'success': True}, 200))
    except Exception as e:
        print(e)
        return make_response(jsonify({'success': False}, 400))