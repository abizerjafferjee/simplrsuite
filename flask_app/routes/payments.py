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

from flask_app.models import *

PaymentRoutes = Blueprint('PaymentRoutes', __name__)

@PaymentRoutes.route('/payment', methods=['POST'])
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
        payment_form = req['body']

        invoices = payment_form['invoices']
        
        for invoice in invoices:
            invoice_record = Invoice.query.get(invoice)
            invoice_record.paid = True

            payment = Payment(
                user = current_user.id,
                supplier_id = payment_form['supplier_id'],
                invoice_id = invoice_record.id,
                payment_type = payment_form['payment_type'],
                receipt = payment_form['receipt'],
                cheque = payment_form['cheque'],
                bank_transfer = payment_form['bank_transfer'],
                date = payment_form['date']
            )

            db.session.add(payment)
            db.session.commit()

        return make_response(jsonify({'success': True}), 200)
    except Exception as e:
        return make_response(jsonify({'success': False}), 400)

@PaymentRoutes.route('/payments', methods=['GET'])
@token_required
def get_payments(current_user):
    """
    Get all payments for this user
    """
    try:
        page = request.args.get('page', type=int)
        per_page = 10
        payments = Payment.query.filter_by(user=current_user.id)\
            .order_by(Payment.created.desc())\
            .paginate(page=page, per_page=per_page, error_out=False)

        schema = PaymentSchema(many=True)
        output = schema.dump(payments.items)
        return make_response(jsonify({'success': True, 'body':output, 'page': payments.page,
                                      'prev': payments.has_prev,
                                      'next': payments.has_next}), 200)
    except Exception as e:
        return make_response(jsonify({'success':False}), 400)


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
                procurement.paid = False
            db.session.delete(payment)
            db.session.commit()
        else:
            pid = payment.procurements
            procurement = Procurement.query.get(int(pid))
            procurement.paid = False
            db.session.delete(payment)
            db.session.commit()

        return make_response(jsonify({'success': True}), 200)
    except Exception as e:
        return make_response(jsonify({'success': False}), 400)

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
    .filter_by(paid=False)\
    .with_entities(func.sum(Procurement.total_cost).label('total_cost'))\
    .all()

    stats['total_outstanding'] = total_outstanding[0][0]

    invoice_outstanding = Procurement.query\
    .filter(Procurement.user==current_user.id)\
    .filter(Procurement.paid==False)\
    .filter(Procurement.invoice!=None)\
    .with_entities(Procurement.invoice)\
    .distinct().all()

    stats['total_invoices'] = len(invoice_outstanding)

    uninvoiceed_outstand = Procurement.query\
    .filter(Procurement.user==current_user.id)\
    .filter(Procurement.paid==False)\
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

    return make_response(jsonify({'success': True, 'messe': 'hello', 'body':stats}), 200)