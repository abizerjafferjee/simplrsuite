from flask import Flask, Blueprint, render_template, abort, jsonify, request, session, make_response
import json
from datetime import datetime
from werkzeug.utils import secure_filename
import os, sys
from flask_app.auth_decorator import token_required

from flask_app.models import *

InvoiceRoutes = Blueprint('InvoiceRoutes', __name__)

@InvoiceRoutes.route('/invoice', methods=['POST'])
@token_required
def add_invoice(current_user):
    """
    adds invoice, adds invoice items to procurement, updates inventory, adds payment
    """
    try:
        invoice = json.loads(request.data)['body']

        items = invoice['items']
        is_paid = invoice['paid']

        # create invoice
        invoice_form = Invoice(
            user = current_user.id,
            supplier_id = invoice['supplier'],
            invoice_number = invoice['invoice'],
            currency = invoice['currency'],
            total_tax = invoice['total_tax'],
            total_cost = invoice['total_cost'],
            date = invoice['date'],
            paid = invoice['paid'],
            terms = invoice['terms'],
            delivery_number = invoice['delivery']
        )

        db.session.add(invoice_form)
        db.session.flush()
        # print(invoice_form.id)

        for item in items:
            # create procurement form
            procurement_form = Procurement(
                user = current_user.id,
                product_id = item['product'],
                invoice_id = invoice_form.id,
                quantity = item['quantity'],
                currency = invoice['currency'],
                unit_cost = item['unit_cost'],
                unit_tax = item['tax'],
                total_cost = item['total_cost']
            )

            db.session.add(procurement_form)
            
            # update inventory
            inventory_form = Inventory.query.filter(Inventory.user==current_user.id)\
                                       .filter(Inventory.product_id == item['product'])\
                                       .first()
            
            if inventory_form:
                inventory_form.quantity += float(item['quantity'])
            else:
                inventory_form = Inventory(
                    user = current_user.id,
                    product_id = item['product'],
                    quantity = float(item['quantity'])
                )
                db.session.add(inventory)

        # create payment
        if is_paid:
            payment = invoice['payment']

            payment_form = Payment(
                user = current_user.id,
                supplier_id = invoice['supplier'],
                invoice_id = invoice_form.id,
                payment_type = payment['payment_type'],
                cheque = payment['cheque'],
                bank_transfer = payment['bank_transfer'],
                receipt = payment['receipt'],
                date = payment['date']
            )

            db.session.add(payment_form)
        
        db.session.commit()
        
        return make_response(jsonify({'success': True}), 200)
    except Exception as e:
        return make_response(jsonify({'success': False}), 400)

@InvoiceRoutes.route('/invoices', methods=['GET'])
@token_required
def get_invoices(current_user):
    """
    Get all invoices for this user
    """
    try:
        page = request.args.get('page', type=int)
        per_page = 10
        invoices = Invoice.query.filter_by(user=current_user.id)\
            .order_by(Invoice.created.desc())\
            .paginate(page=page, per_page=per_page, error_out=False)

        schema = InvoiceSchema(many=True)
        output = schema.dump(invoices.items)
        
        return make_response(jsonify({'success': True, 'body':output, 'page': invoices.page,
                                      'prev': invoices.has_prev,
                                      'next': invoices.has_next}), 200)
    except Exception as e:
        return make_response(jsonify({'success':False}), 400)

@InvoiceRoutes.route('/invoices/<int:id>', methods=['GET'])
@token_required
def get_supplier_outstanding_invoices(current_user, id):
    """
    Return distinct invoices which are unpaid for a given supplier id
    """
    invoices = Invoice.query\
        .filter(Invoice.user==current_user.id)\
        .filter(Invoice.supplier_id==id)\
        .filter(Invoice.paid==False)\
        .all()
    
    schema = InvoiceSchema(many=True)
    output = schema.dump(invoices)

    return make_response(jsonify({'success': True, 'body': output}), 200)

@InvoiceRoutes.route('/invoices/numbers', methods=['GET'])
@token_required
def get_invoice_numbers(current_user):
    """
    Get all invoice numbers for this user
    """
    try:
        invoices = Invoice.query.filter_by(user=current_user.id).all()

        invoice_numbers = []
        for invoice in invoices:
            invoice_numbers.append({
                'id': invoice.id,
                'text': invoice.invoice_number
            })
        
        return make_response(jsonify({'success': True, 'body':invoice_numbers}), 200)
    except Exception as e:
        return make_response(jsonify({'success':False}), 400)

@InvoiceRoutes.route('/invoices/outstanding', methods=['GET'])
@token_required
def get_invoices_outstanding(current_user):
    """
    Get all invoices for this user
    """
    try:
        page = request.args.get('page', type=int)
        per_page = 10
        invoices = Invoice.query.filter_by(user=current_user.id, paid=False)\
            .order_by(Invoice.created.desc())\
            .paginate(page=page, per_page=per_page, error_out=False)

        schema = InvoiceSchema(many=True)
        output = schema.dump(invoices.items)
        
        return make_response(jsonify({'success': True, 'body':output, 'page': invoices.page,
                                      'prev': invoices.has_prev,
                                      'next': invoices.has_next}), 200)
    except Exception as e:
        return make_response(jsonify({'success':False}), 400)
