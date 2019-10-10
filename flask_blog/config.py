import os, json

config_json = json.load(open('config.json'))
# Use the next line instead for the web server (pythonanywhere)
# config_json = json.load(open('/home/flaskblog/site/flask-blog/flask_blog/config.json'))

class Config:
    SECRET_KEY = config_json['SECRET_KEY']
    SQLALCHEMY_DATABASE_URI = config_json['DATABASE']
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = config_json['MAIL_USERNAME']
    MAIL_PASSWORD = config_json['MAIL_PASSWORD']

# class Config:
#     SECRET_KEY = os.environ.get('FLASKBLOG_SECRET_KEY')
#     SQLALCHEMY_DATABASE_URI = os.environ.get('FLASKBLOG_DATABASE')
#     MAIL_SERVER = 'smtp.gmail.com'
#     MAIL_PORT = 587
#     MAIL_USE_TLS = True
#     MAIL_USERNAME = os.environ.get('FLASKBLOG_EMAIL_USERNAME')
#     MAIL_PASSWORD = os.environ.get('FLASKBLOG_EMAIL_PASSWORD')