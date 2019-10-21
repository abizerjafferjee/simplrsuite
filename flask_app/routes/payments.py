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

from flask_app.models import db, Inventory, Procurement, Supplier, Payment, InventorySchema, ProcurementSchema, OutstandingPaymentsSchema

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

        # paid_invoices = []

        # all_invoices = body['invoices'].split()
        # for invoice in all_invoices:
        #     rows = Procurement.query.filter_by(invoice=invoice).all()
        #     print(rows)
        #     for row in rows:
        #         if row.paid == "Paid":
        #             paid_invoices.append({'id': row.id, 'invoice': row.invoice})
        #             print(row.paid)
        #         else:
        #             row.paid = "Paid"
        #             db.session.commit()
        
        # # i.e. 
        # if len(paid_invoices) > 0:

        print(body['invoices'])


        # payment = Payment(
        #     supplier_id = body['supplier_id'],
        #     amount = float(body['amount']),
        #     currency = body['currency'],
        #     invoices = body['invoices'],
        #     additional_info = body['additional_info']
        # )
        
        # db.session.add(payment)

        # invoices = body['invoices']
        # db.session.commit()

        return make_response(jsonify({'success': True}, 200))
        
    except Exception as e:
        print(e)
        return make_response(jsonify({'success': False}, 400))


@PaymentRoutes.route('/payments/made', methods=['GET'])
def get_payments_made():
    """
    Return payments that have been made
    """
    return make_response(jsonify({'success': True}, 200))

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
        .with_entities(Procurement.supplier_id, func.sum(Procurement.total_cost).label('total_cost'),func.array_agg(Procurement.invoice).label('invoices'), func.min(Supplier.business_name).label('business_name'))\
        .group_by(Procurement.supplier_id)\
        .paginate(page=page, per_page=per_page, error_out=False)

    schema = OutstandingPaymentsSchema(many=True)
    output = schema.dump(outstanding_by_supplier.items)
    print(output)

    # print(outstanding_by_supplier.items)
    return make_response(jsonify({'success': True, 'body': outstanding_by_supplier.items,
                                  'page': outstanding_by_supplier.page, 'prev': outstanding_by_supplier.has_prev,
                                  'next': outstanding_by_supplier.has_next}, 200))

@PaymentRoutes.route('/payments/due/<int:id>', methods=['GET'])
def get_outstanding_invoices(id):
    """
    Return distinct invoices which are unpaid by supplier
    """
    outstanding_invoices = Procurement.query\
        .filter_by(paid='Unpaid', supplier_id=id)\
        .with_entities(Procurement.invoice).distinct().all()
    
    outstanding_invoices = [invoice[0] for invoice in outstanding_invoices]

    return make_response(jsonify({'success': True, 'body': outstanding_invoices}, 200))