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

from flask_app.models import db, Inventory, Procurement, Supplier, Payment,\
InventorySchema, ProcurementSchema, PaymentSchema, OutstandingPaymentsSchema,\
OutstandingPaymentsSupplierSchema

PaymentRoutes = Blueprint('PaymentRoutes', __name__)

@PaymentRoutes.route('/payments', methods=['POST'])
def record_payment():
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

        paid_invoices = body['invoices']
        # print(paid_invoices)

        for invoice in paid_invoices:
            procurements = Procurement.query.filter_by(invoice=invoice).all()
            for procurement in procurements:
                procurement.paid = "Paid"
                db.session.commit()

        payment = Payment(
            supplier_id = body['supplier_id'],
            amount = float(body['amount']),
            currency = body['currency'],
            invoices = body['invoices'],
            additional_info = body['additional_info']
        )
        
        db.session.add(payment)
        db.session.commit()

        return make_response(jsonify({'success': True}, 200))
        
    except Exception as e:
        print(e)
        return make_response(jsonify({'success': False}, 400))


@PaymentRoutes.route('/payments/made', methods=['GET'])
def get_payments_made():
    """
    Return payments that have been made
    """
    per_page = 10
    page = request.args.get('page', type=int)
    payments = Payment.query.paginate(page=page, per_page=per_page, error_out=False)
    schema = PaymentSchema(many=True)
    output = schema.dump(payments.items)
    print(payments.items)
    print(output)
    return make_response(jsonify({'success': True, 'body':output, 'page': payments.page,
                                  'prev': payments.has_prev, 'next': payments.has_next}, 200))

@PaymentRoutes.route('/payments/due', methods=['GET'])
def get_payments_due():
    """
    Return payments that are due. A list of suppliers and the outstanding amounts
    i.e procurement records with Paid == 'Unpaid'.
    """
    per_page = 10
    page = request.args.get('page', type=int)
    outstanding_by_supplier = Procurement.query\
        .filter_by(paid='Unpaid')\
        .join(Supplier, Procurement.supplier_id==Supplier.id)\
        .with_entities(Procurement.supplier_id, 
                       func.sum(Procurement.total_cost).label('total_cost'),
                       func.array_agg(Procurement.invoice).label('invoices'),
                       func.min(Supplier.business_name).label('business_name'))\
        .group_by(Procurement.supplier_id)\
        .paginate(page=page, per_page=per_page, error_out=False)

    schema = OutstandingPaymentsSchema(many=True)
    output = schema.dump(outstanding_by_supplier.items)
    # print(output)

    # print(outstanding_by_supplier.items)
    return make_response(jsonify({'success': True, 'body': outstanding_by_supplier.items,
                                  'page': outstanding_by_supplier.page, 'prev': outstanding_by_supplier.has_prev,
                                  'next': outstanding_by_supplier.has_next}, 200))

@PaymentRoutes.route('/payments/due/<int:id>', methods=['GET'])
def get_outstanding_invoices(id):
    """
    Return distinct invoices which are unpaid by supplier
    """
    supplier_outstanding = Procurement.query\
        .filter_by(paid='Unpaid', supplier_id=id)\
        .with_entities(Procurement.invoice,
                       func.sum(Procurement.total_cost).label('total_cost'),
                       func.min(Procurement.created).label('created'))\
        .group_by(Procurement.invoice)\
        .all()
    
    schema = OutstandingPaymentsSupplierSchema(many=True)
    output = schema.dump(supplier_outstanding)
    # print(output)

    return make_response(jsonify({'success': True, 'body': output}, 200))