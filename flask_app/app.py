import os, sys
sys.path.append('../')
from flask import Flask, jsonify, request, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS

# internal imports
from flask_app.config import *

app = Flask(__name__)
if os.environ.get('FLASK_ENVIRONMENT') == 'PROD':
    app.config.from_object(ProductionConfig)
else:
    app.config.from_object(DevelopmentConfig)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app, engine_options=app.config['SQLALCHEMY_ENGINE_OPTIONS'])
ma = Marshmallow(app)

# enable CORS
cors = CORS(app)

@app.route('/api')
def index():
    return '<h1>Simplr Suite is lives</h1>'

from flask_app.views import *

if __name__ == "__main__":
    # port = os.getenv('PORT', '5000')
    # app.run(host='localhost', port=int(port), threaded=True)
    app.run(host='0.0.0.0')