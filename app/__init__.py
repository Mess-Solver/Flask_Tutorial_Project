from flask import Flask
from .config import Config
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail
from flask_marshmallow import Marshmallow

import os
basedir=os.path.abspath(os.path.dirname(__file__))

app=Flask(__name__)





app.config.from_object(Config)
login=LoginManager(app)
app.config['SQLALCHEMY_DATABASE_URI']=os.environ.get("DATABASE_URL") or \
                             'sqlite:///' + os.path.join(basedir, 'app.db')


app.config.update(

#EMAIL SETTINGS
	MAIL_SERVER='smtp.gmail.com',
	MAIL_PORT=465,
	MAIL_USE_SSL=True,
	MAIL_USERNAME = 'kamranhaider034@gmail.com',
	MAIL_PASSWORD = 'progressive'
)

mail=Mail(app)
login.login_view="login"
db=SQLAlchemy(app)
migrate=Migrate(app,db)
ma=Marshmallow(app)

from . import routes,models,api