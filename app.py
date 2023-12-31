from flask import Flask
from config import *
from models.models import db
from api.api import initialize_app
from flask_cors import CORS

app = Flask(__name__)
app.secret_key = 'mysecretkey123'



app.config["SQLALCHEMY_DATABASE_URI"] = f'mysql+mysqlconnector://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}'
app.config['SESSION_COOKIE_SAMESITE'] = 'None'
app.config['SESSION_COOKIE_SECURE'] = True
db.init_app(app)
app.debug = True

CORS(app, resources={r"/api/*": {"origins": "*"}})

initialize_app(app)
if __name__ == '__main__':
    app.run()
