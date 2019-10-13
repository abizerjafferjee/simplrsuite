import os, sys
sys.path.append('../')
from flask import Flask, jsonify, request, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS

# internal imports
from flask_app.config import Config

app = Flask(__name__)
app.config.from_object(Config)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
ma = Marshmallow(app)

# enable CORS
cors = CORS(app)

from flask_app.views import *

port = os.getenv('PORT', '5000')
if __name__ == "__main__":
    app.run(debug=False, host='localhost', port=int(port), threaded=True)