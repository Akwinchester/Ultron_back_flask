from flask import Flask
from config import *
from models import db
from api import initialize_app

app = Flask(__name__)
app.secret_key = 'mysecretkey123'


app.config["SQLALCHEMY_DATABASE_URI"] = f'mysql+mysqlconnector://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}'
db.init_app(app)
app.debug = True

initialize_app(app)
if __name__ == '__main__':
    app.run()
