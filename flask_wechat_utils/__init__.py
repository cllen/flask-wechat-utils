#coding:utf8

#frame
from flask import Blueprint
from flask_restplus import Api
from flask_mongoengine import MongoEngine

import config


def init_app(app):

	print app.config.get('WXAPP_ID')

	config.WEB_NAME = 'myweb' if not app.config.get('WEB_NAME') else app.config.get('WEB_NAME')

	config.WXAPP_ID = None if not app.config.get('WXAPP_ID') else app.config.get('WXAPP_ID')
	config.WXAPP_SECRET = None if not app.config.get('WXAPP_SECRET') else app.config.get('WXAPP_SECRET')

	config.TOKEN_SECRET_KEY = 'xxx' if not app.config.get('TOKEN_SECRET_KEY') else app.config.get('TOKEN_SECRET_KEY')
	config.TOKEN_SALT = 'xxx' if not app.config.get('TOKEN_SALT') else app.config.get('TOKEN_SALT')
	config.TOKEN_TIMEOUT_HOURS = 24 * 365 if not app.config.get('TOKEN_TIMEOUT_HOURS') else app.config.get('TOKEN_TIMEOUT_HOURS')
	config.TOKEN_FIELDS_REQUIRED = ['openid'] if not app.config.get('TOKEN_FIELDS_REQUIRED') else app.config.get('TOKEN_FIELDS_REQUIRED')

	config.TOKEN_HEADER_FIELD = 'token' if not app.config.get('TOKEN_HEADER_FIELD') else app.config.get('TOKEN_HEADER_FIELD')
	config.LOGIN_CODE_FIELD_NAME = 'code' if not app.config.get('LOGIN_CODE_FIELD_NAME') else app.config.get('LOGIN_CODE_FIELD_NAME')
	config.UPDATE_IV_FIELD_NAME = 'iv' if not app.config.get('UPDATE_IV_FIELD_NAME') else app.config.get('UPDATE_IV_FIELD_NAME')
	config.UPDATE_ENCRYPTEDDATA_FIELD_NAME = 'encryptedData' if not app.config.get('UPDATE_ENCRYPTEDDATA_FIELD_NAME') else app.config.get('UPDATE_ENCRYPTEDDATA_FIELD_NAME')
	config.TEMPLATE_ID = None if not app.config.get('TEMPLATE_ID') else app.config.get('TEMPLATE_ID')

	init_db(app)
	init_bp(app)
	init_api(app)

	app.register_blueprint(config.bp)
	

def init_db(app):
	config.db = MongoEngine()
	config.db.init_app(app)

def init_bp(app):
	config.bp = Blueprint(
		app.config['WEB_NAME'], 
		__name__, 
		url_prefix='/{}'.format(app.config['WEB_NAME'])
	)
	return config.bp

def init_api(app):
	config.api = Api(
		config.bp, 
		version='0.1', 
		title='{} API'.format(app.config['WEB_NAME']),
		description='description',
	)

