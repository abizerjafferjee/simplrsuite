from flask import Flask, Blueprint, render_template, abort, jsonify, request, session, make_response
import json
from datetime import datetime
from werkzeug.utils import secure_filename
import os, sys
from flask_app.auth_decorator import token_required

from flask_app.models import db, MailList, MailListSchema

MailListRoutes = Blueprint('MailListRoutes', __name__)

@MailListRoutes.route('/mailer/add', methods=['POST'])
@token_required
def add_mailer(current_user):
        try:
            body = json.loads(request.data)['body']
            new_mailer = MailList(
                user = current_user.id,
                name = body['name'],
                business = body['business'],
                email = body['email'],
                phone = body['phone'],
                remark = body['remark']
            )
            db.session.add(new_mailer)
            db.session.commit()
            mail_schema = MailListSchema()
            output = mail_schema.dump(new_mailer)
            return make_response(jsonify({'success': True, 'mailer':output}, 200))
        except Exception as e:
            print(e)
            return make_response(jsonify({'success': False, 'error': 'Unable to get data. Please make sure input is valid.'}, 400))
