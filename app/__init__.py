from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
import logging, os
from logging.handlers import SMTPHandler, RotatingFileHandler 

app1 = Flask(__name__)
app1.config.from_object(Config)
db = SQLAlchemy(app1)
migrate = Migrate(app1, db)
login = LoginManager(app1)
login.login_view = 'login'

from app import routes, models, errors

if not app1.debug: #enabled email logger only when the applicaiton is running without debug mode and next line when the email server exists in the program
    if app1.config['MAIL_SERVER']:
        auth = None
        if app1.config['MAIL_USERNAME'] or app1.config['MAIL_PASSWORD']:
            auth = (app1.config['MAIL_USERNAME'], app1.config['MAIL_PASSWORD'])
        secure = None
        if app1.config['MAIL_USE_TLS']:
            secure = ()
        mail_handler = SMTPHandler(
            mailhost=(app1.config['MAIL_SERVER'], app1.config['MAIL_PORT']),
            fromaddr='no-reply@' + app1.config['MAIL_SERVER'],
            toaddrs=app1.config['ADMINS'], subject='Microblog Failure',
            credentials=auth, secure=secure)
        mail_handler.setLevel(logging.ERROR)
        app1.logger.addHandler(mail_handler)
    
    if not os.path.exists('logs'): #log file for app, this time of type RotatingFileHandler, needs to be attached to the application logger, in a similar way to the email handler.
        os.mkdir('logs') #write log file name microblog.log in logs directory which is created if not existing
    file_handler = RotatingFileHandler('logs/microblog.log', maxBytes=10240,
                                       backupCount=10) #RotatingFileHandler class rotates log so log files dont grow too large, here limiting size to 10KB, keeping last ten log files as backup
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')) #loffingformatter custom formatter for log msg including timestamp, logginglevel, source and line number
    file_handler.setLevel(logging.INFO) #make logging useful with categories debug,info,warning,error and critical in increasing order
    app1.logger.addHandler(file_handler)

    app1.logger.setLevel(logging.INFO)
    app1.logger.info('Microblog startup')

