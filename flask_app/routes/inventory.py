from flask import Flask, Blueprint, render_template, abort, jsonify, request, session, make_response
import json
from datetime import datetime
from werkzeug.utils import secure_filename
import os, sys

from flask_app.models import db, Inventory, Procurement, Supplier, Product, InventorySchema, ProcurementSchema

InventoryRoutes = Blueprint('InventoryRoutes', __name__)

@InventoryRoutes.route('/inventory', methods=['POST'])
def add_inventory():
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
            # db.session.commit()

        procurement = Procurement(
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

@InventoryRoutes.route('/inventory', methods=['PUT'])
def edit_inventory():
    return make_response(jsonify({'success': True}, 200))

@InventoryRoutes.route('/inventory', methods=['DELETE'])
def delete_inventory():
    return make_response(jsonify({'success': True}, 200))


#######################################################
# Procurements
#######################################################
@InventoryRoutes.route('/procurement', methods=['GET'])
def get_procurement():
    """
    get the 10 latest procurement records
    """
    try:
        latest_records = 10
        procurements = Procurement.query.order_by(Procurement.id.desc()).limit(latest_records).all()
        procurement_schema = ProcurementSchema(many=True)
        output = procurement_schema.dump(procurements)
        return make_response(jsonify({'success': True, 'body':output}, 200))
    except Exception as e:
        print(e)

@InventoryRoutes.route('/procurement', methods=['PUT'])
def edit_procurement():
    """
    edit a procurement record from the 10 latest procurement records
    update the inventory model as well, if the inventory quantity has changed
    """
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
        inventory_record = Inventory.query.filter_by(product_id = product).first()
        inventory_record.quantity = inventory_record.quantity - procurement.quantity + quantity
        procurement.quantity = quantity
    
    procurement.invoice = invoice
    procurement.unit_cost = unit_cost
    procurement.total_cost = total_cost

    db.session.commit()

    return make_response(jsonify({'success': True}, 200))

@InventoryRoutes.route('/procurement', methods=['DELETE'])
def delete_procurement():
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