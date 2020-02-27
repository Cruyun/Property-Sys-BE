from flask import Flask
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_pagedown import  PageDown
from config import config

moment=Moment()
db = SQLAlchemy()
pagedown=PageDown()

login_manager=LoginManager()
login_manager.session_protection = 'strong'

def create_app(config_name=None,main=True):
  if config_name is None:
    config_name = 'default'
  app=Flask(__name__)
  app.config.from_object(config[config_name])
  config[config_name].init_app(app)

  with app.app_context():
    db.init_app(app)

  moment.init_app(app)
  db.init_app(app)
  login_manager.init_app(app)
  pagedown.init_app(app)

  from .api import api as api_blueprint
  app.register_blueprint(api_blueprint,url_prefix="/api/v1.0")
  return app

app = create_app(config_name = 'default')

#from .api import api as api_blueprint
#app.register_blueprint(api_blueprint,url_prefix="/api/v1.0")
