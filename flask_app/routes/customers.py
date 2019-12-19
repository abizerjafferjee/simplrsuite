from flask import Flask, Blueprint, render_template, abort, jsonify, request, session, make_response
import json
from datetime import datetime
from werkzeug.utils import secure_filename
import os, sys
from flask_app.auth_decorator import token_required

from flask_app.models import db, MailList, MailListSchema

CustomerRoutes = Blueprint('CustomerRoutes', __name__)

@CustomerRoutes.route('/maillist', methods=['POST'])
@token_required
def add(current_user):
    """
    Handles post request for adding new supplier.
    """
    try:
        req = json.loads(request.data)
        body = req['body']
        maillist = MailList(
            user = current_user.id,
            name = body['name'],
            business = body['business'],
            email = body['email'],
            phone = body['phone_code'] + body['phone'],
            remark = body['remark']
        )
        
        db.session.add(maillist)
        db.session.commit()
        return make_response(jsonify({'success': True}), 200)
        
    except Exception as e:
        print(e)
        return make_response(jsonify({'success': False}), 400)

@CustomerRoutes.route('/maillist', methods=['GET'])
@token_required
def get(current_user):
    """
    Handles get request for getting a supplier by id, post request for adding
    new supplier and put request for editing a supplier's information.
    """
    # try:
    page = request.args.get('page', type=int)
    per_page = 12

    maillist = MailList.query\
        .filter(MailList.user==current_user.id)\
        .order_by(MailList.created.desc())\
        .paginate(page=page, per_page=per_page, error_out=False)
    schema = MailListSchema(many=True)
    output = schema.dump(maillist.items)
    return make_response(jsonify({'success': True, 'body': output,'body': output,
                                    'page': maillist.page, 'prev': maillist.has_prev,
                                    'next': maillist.has_next}), 200)

    # except Exception as e:
    #     print(e)
    #     return make_response(jsonify({'success': False}, 400))