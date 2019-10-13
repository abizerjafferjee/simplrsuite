from flask_app.app import app
from flask import render_template, jsonify, request, redirect, url_for, flash, make_response

from werkzeug.utils import secure_filename
from datetime import datetime
import json
import pandas as pd
from numpy import genfromtxt

from flask_app.routes.products import ProductRoutes
from flask_app.routes.category import CategoryRoutes
from flask_app.routes.suppliers import SupplierRoutes
from flask_app.routes.inventory import InventoryRoutes
from flask_app.routes.maillist import MailListRoutes

app.register_blueprint(ProductRoutes)
app.register_blueprint(CategoryRoutes)
app.register_blueprint(SupplierRoutes)
app.register_blueprint(InventoryRoutes)
app.register_blueprint(MailListRoutes)

from flask_app.models import *
