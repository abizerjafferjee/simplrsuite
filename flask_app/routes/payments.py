from flask_app.app import app
from flask import Flask, Blueprint, render_template, abort, jsonify, request, session, make_response
import json
from datetime import datetime
from werkzeug.utils import secure_filename
import os, sys
import string
import random
import re
from sqlalchemy import func
from flask_app.auth_decorator import token_required

from flask_app.models import db, Inventory, Procurement, Supplier, Payment,\
InventorySchema, ProcurementSchema, PaymentSchema, OutstandingPaymentsSchema,\
OutstandingPaymentsSupplierSchema

PaymentRoutes = Blueprint('PaymentRoutes', __name__)

@PaymentRoutes.route('/payments', methods=['POST'])
@token_required
def record_payment(current_user):
    """
    Handles post request for recording a payment.
    * test whether adding payment record before
    processing invoices and commiting after everything
    means that the payment is recorded even when
    the invoices failure to process.
    """
    try:
        req = json.loads(request.data)
        body = req['body']
        _from = req['from']

        # from record payment form
        if _from == 'form': 

            # get all unique invoices
            paid_invoices = []
            for invoice in body['invoices']:
                if invoice not in paid_invoices:
                    paid_invoices.append(invoice)

            for invoice in paid_invoices:
                procurements = Procurement.query.filter_by(invoice=invoice).all()
                for procurement in procurements:
                    procurement.paid = "Paid"
                    db.session.commit()

            supplier = Supplier.query.get(body['supplier_id'])

            payment = Payment(
                user = current_user.id,
                supplier_id = supplier,
                amount = float(body['amount']),
                currency = body['currency'],
                invoices = ",".join(body['invoices']),
                additional_info = body['additional_info']
            )
            
            db.session.add(payment)
            db.session.commit()

        # clicked "record as paid" from payment view
        elif _from == 'view-invoiced':

            # get all unique invoices
            paid_invoices = []
            for invoice in body['invoices']:
                if invoice not in paid_invoices:
                    paid_invoices.append(invoice)

            for invoice in paid_invoices:
                procurements = Procurement.query.filter_by(invoice=invoice).all()
                for procurement in procurements:
                    procurement.paid = "Paid"
                    db.session.commit()

            supplier = Supplier.query.get(body['supplier_id'])

            payment = Payment(
                user = current_user.id,
                supplier_id = supplier.id,
                amount = float(body['total_cost']),
                currency = 'TZS',
                invoices = ",".join(paid_invoices)
            )

            db.session.add(payment)
            db.session.commit()

        elif _from == 'view-uninvoiced':

            procurement = Procurement.query.get(body['id'])
            procurement.paid = "Paid"
            db.session.commit()

            supplier = Supplier.query.get(body['supplier'])

            payment = Payment(
                user = current_user.id,
                supplier_id = supplier.id,
                amount = float(body['total_cost']),
                procurements = str(body['id']),
                invoiced = False,
                currency = body['currency'],
            )
            db.session.add(payment)
            db.session.commit()

        return make_response(jsonify({'success': True}, 200))
        
    except Exception as e:
        print(e)
        return make_response(jsonify({'success': False}, 400))

@PaymentRoutes.route('/payment/<int:id>', methods=['DELETE'])
@token_required
def delete_payment(current_user, id):
    """
    Delete a procurement record in db by id
    subtract the procurement quantity from inventory
    """
    try:
        payment = Payment.query.get(id)
        if payment.invoiced == True:
            invoices = payment.invoices.split(',')
            procurements = Procurement.query.filter(Procurement.invoice.in_(invoices))
            for procurement in procurements:
                procurement.paid = 'Unpaid'
            db.session.delete(payment)
            db.session.commit()
        else:
            pid = payment.procurements
            procurement = Procurement.query.get(int(pid))
            procurement.paid = "Unpaid"
            db.session.delete(payment)
            db.session.commit()

        return make_response(jsonify({'success': True}, 200))
    except Exception as e:
        print(e)
        return make_response(jsonify({'success': False}, 400))

@PaymentRoutes.route('/payments/made', methods=['GET'])
@token_required
def get_payments_made(current_user):
    """
    Return payments that have been made
    """
    per_page = 10
    page = request.args.get('page', type=int)
    payments = Payment.query\
        .filter(Payment.user==current_user.id)\
        .order_by(Payment.created.desc())\
        .paginate(page=page, per_page=per_page, error_out=False)
    schema = PaymentSchema(many=True)
    output = schema.dump(payments.items)
    return make_response(jsonify({'success': True, 'body':output, 'page': payments.page,
                                  'prev': payments.has_prev, 'next': payments.has_next}, 200))

@PaymentRoutes.route('/payments/due', methods=['GET'])
@token_required
def get_invoices_due(current_user):
    """
    Return payments that are due. A list of suppliers and the outstanding amounts
    i.e procurement records with Paid == 'Unpaid'.
    """
    per_page = 10
    page = request.args.get('page', type=int)
    outstanding_by_supplier = Procurement.query\
        .filter(Procurement.user==current_user.id)\
        .filter(Procurement.paid=='Unpaid')\
        .filter(Procurement.invoice != None)\
        .join(Supplier, Procurement.supplier_id==Supplier.id)\
        .with_entities(Procurement.supplier_id, 
                       func.sum(Procurement.total_cost).label('total_cost'),
                       func.array_agg(Procurement.invoice).label('invoices'),
                       func.min(Supplier.business_name).label('business_name'))\
        .group_by(Procurement.supplier_id)\
        .paginate(page=page, per_page=per_page, error_out=False)

    return make_response(jsonify({'success': True, 'body': outstanding_by_supplier.items,
                                  'page': outstanding_by_supplier.page, 'prev': outstanding_by_supplier.has_prev,
                                  'next': outstanding_by_supplier.has_next}, 200))

@PaymentRoutes.route('/payments/due/uninvoiced', methods=['GET'])
@token_required
def get_uninvoiced_due(current_user):
    """
    Return payments that are due for procurements without invoices.
    A list of procurments and the outstanding amounts
    i.e procurement records with Paid == 'Unpaid' and invoice == None.
    """
    per_page = 10
    page = request.args.get('page', type=int)
    outstanding_by_procurement = Procurement.query\
        .filter(Procurement.user==current_user.id)\
        .filter(Procurement.paid=='Unpaid')\
        .filter(Procurement.invoice == None)\
        .join(Supplier, Procurement.supplier_id==Supplier.id)\
        .order_by(Procurement.created.desc())\
        .paginate(page=page, per_page=per_page, error_out=False)

    schema = ProcurementSchema(many=True)
    output = schema.dump(outstanding_by_procurement.items)
    return make_response(jsonify({'success': True, 'body': output,
                                  'page': outstanding_by_procurement.page, 'prev': outstanding_by_procurement.has_prev,
                                  'next': outstanding_by_procurement.has_next}, 200))

@PaymentRoutes.route('/payments/due/<int:id>', methods=['GET'])
@token_required
def get_outstanding_invoices(current_user, id):
    """
    Return distinct invoices which are unpaid by supplier
    """
    supplier_outstanding = Procurement.query\
        .filter(Procurement.user==current_user.id)\
        .filter_by(paid='Unpaid', supplier_id=id)\
        .with_entities(Procurement.invoice,
                       func.sum(Procurement.total_cost).label('total_cost'),
                       func.min(Procurement.created).label('created'))\
        .group_by(Procurement.invoice)\
        .all()
    
    schema = OutstandingPaymentsSupplierSchema(many=True)
    output = schema.dump(supplier_outstanding)

    return make_response(jsonify({'success': True, 'body': output}, 200))

@PaymentRoutes.route('/payments/stats', methods=['GET'])
@token_required
def get_payment_stats(current_user):
    """
    Return total amount due, total outstanding invoices,
    total procurments without invoices, last payment details
    """
    stats = {}

    total_outstanding = Procurement.query\
    .filter(Procurement.user==current_user.id)\
    .filter_by(paid='Unpaid')\
    .with_entities(func.sum(Procurement.total_cost).label('total_cost'))\
    .all()

    stats['total_outstanding'] = total_outstanding[0][0]

    invoice_outstanding = Procurement.query\
    .filter(Procurement.user==current_user.id)\
    .filter(Procurement.paid=='Unpaid')\
    .filter(Procurement.invoice!=None)\
    .with_entities(Procurement.invoice)\
    .distinct().all()

    stats['total_invoices'] = len(invoice_outstanding)

    uninvoiceed_outstand = Procurement.query\
    .filter(Procurement.user==current_user.id)\
    .filter(Procurement.paid=='Unpaid')\
    .filter(Procurement.invoice==None)\
    .with_entities(func.sum(Procurement.total_cost).label('total_cost'))\
    .all()

    stats['uninvoiced_outstanding'] = uninvoiceed_outstand[0][0] if not None else 0

    latest_payment = Payment.query\
    .filter(Payment.user==current_user.id)\
    .order_by(Payment.created.desc())\
    .limit(1)\
    .all()

    schema = PaymentSchema()
    latest_payment = schema.dump(latest_payment[0] if len(latest_payment) > 0 else None)
    stats['latest_payment'] = latest_payment

    return make_response(jsonify({'success': True, 'messe': 'hello', 'body':stats}, 200))

@PaymentRoutes.route('/payments/supplier/<int:id>', methods=['GET'])
@token_required
def get_payments_by_supplier(current_user, id):
    """
    Get payments from db by supplier id
    """
    try:
        page = request.args.get('page', type=int)
        per_page = 10
        payments = Payment.query.filter(Payment.user==current_user.id)\
            .filter(Payment.supplier_id == id)\
            .order_by(Payment.created.desc())\
            .paginate(page=page, per_page=per_page, error_out=False)
        schema = PaymentSchema(many=True)
        output = schema.dump(payments.items)
        return make_response(jsonify({'success':True, 'body':output,
                                      'page': payments.page,
                                      'prev': payments.has_prev,
                                      'next': payments.has_next}, 200))
    except Exception as e:
        print(e)
        return make_response(jsonify({'success':False}, 400))