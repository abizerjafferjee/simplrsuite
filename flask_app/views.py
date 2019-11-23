from flask_app.app import app
from flask import render_template, jsonify, request, redirect, url_for, flash, make_response

from werkzeug.utils import secure_filename
from datetime import datetime
import json
# import pandas as pd
# from numpy import genfromtxt

from flask_app.routes.auth import AuthRoutes
from flask_app.routes.products import ProductRoutes
from flask_app.routes.category import CategoryRoutes
from flask_app.routes.suppliers import SupplierRoutes
from flask_app.routes.inventory import InventoryRoutes
from flask_app.routes.payments import PaymentRoutes
from flask_app.routes.customers import CustomerRoutes

prefix = '/api'

app.register_blueprint(AuthRoutes, url_prefix=prefix)
app.register_blueprint(ProductRoutes, url_prefix=prefix)
app.register_blueprint(CategoryRoutes, url_prefix=prefix)
app.register_blueprint(SupplierRoutes, url_prefix=prefix)
app.register_blueprint(InventoryRoutes, url_prefix=prefix)
app.register_blueprint(PaymentRoutes, url_prefix=prefix)
app.register_blueprint(CustomerRoutes, url_prefix=prefix)

from flask_app.models import *