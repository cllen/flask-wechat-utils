#coding:utf8

#frame
from flask import Blueprint
from flask_restplus import Api
from flask_mongoengine import MongoEngine

#wechat
from config import WEB_NAME


bp = Blueprint(
	WEB_NAME, 
	__name__, 
	url_prefix='/{}'.format(WEB_NAME)
)

api = Api(
	bp, 
	version='0.1', 
	title='{} API'.format(WEB_NAME),
	description='description',
)

db = MongoEngine()

#routes
# from user import routes
# from message_template import routes
