from flask import Flask
from os import getenv
from flask_sqlalchemy import SQLAlchemy



app = Flask(__name__)
app.secret_key = getenv("SECRET_KEY")

import routes







    


