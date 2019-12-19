from flask import Flask, Blueprint, render_template, abort, jsonify, request, session, make_response
import json
from datetime import datetime
from werkzeug.utils import secure_filename
import os, sys
from flask_app.auth_decorator import token_required

from flask_app.models import *

InventoryRoutes = Blueprint('InventoryRoutes', __name__)

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
        
        return make_response(jsonify({'success':True, 'body':output}), 200)
    except Exception as e:
        return make_response(jsonify({'success':False}), 400)

@InventoryRoutes.route('/inventory', methods=['PUT'])
@token_required
def edit_inventory(current_user):
    try:
        id = request.args.get('id', type=int)
        updatedInventory = json.loads(request.data)['body']
        d = Inventory.query.get(id)
        d.quantity = float(updatedInventory['quantity'])
        db.session.commit()
        return make_response(jsonify({'success': True}), 200)
    except Exception as e:
        return make_response(jsonify({'success': False}), 400)

@InventoryRoutes.route('/inventory/<int:id>', methods=['DELETE'])
@token_required
def delete_inventory(current_user, id):
    try:
        inventory = Inventory.query\
            .filter(Inventory.user==current_user.id)\
            .filter_by(product_id = id).delete()
        db.session.commit()
        return make_response(jsonify({'success': True}), 200)
    except Exception as e:
        return make_response(jsonify({'success': False}), 400)