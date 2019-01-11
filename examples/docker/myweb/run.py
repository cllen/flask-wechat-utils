#coding:utf8
from flask import Flask

from flask_wechat_utils import bp as wechat_user_auth_bp
from flask_wechat_utils import db as wechat_user_auth_db
from flask_wechat_utils import config as wechat_config

from blog.routes import bp as blog_bp
from user.routes import bp as user_bp

#-------------------------------------------
# app
#-------------------------------------------
app = Flask(__name__)

#-------------------------------------------
# config
#-------------------------------------------
app.config['MONGODB_SETTINGS'] = {
	'db': 'xxx',
	'host': 'mongo',
	'port': 27017,
}

wechat_config.WXAPP_ID = 'xxx'
wechat_config.WXAPP_SECRET = 'xxx'
wechat_config.WEB_NAME = 'myweb'
wechat_config.TOKEN_SECRET_KEY = 'xxx'
wechat_config.TOKEN_SALT = 'xxx'
wechat_config.TOKEN_TIMEOUT_HOURS = 24 * 365
wechat_config.TOKEN_FIELDS_REQUIRED = ['openid']

wechat_config.TOKEN_HEADER_FIELD = 'token'
wechat_config.LOGIN_CODE_FIELD_NAME = 'code'
wechat_config.UPDATE_IV_FIELD_NAME = 'iv'
wechat_config.UPDATE_ENCRYPTEDDATA_FIELD_NAME = 'encryptedData'

#-------------------------------------------
# blueprint/db
#-------------------------------------------
wechat_user_auth_db.init_app(app)

app.register_blueprint(user_bp)
app.register_blueprint(blog_bp)


if __name__ == '__main__':
	app.run(host='0.0.0.0',port=5000)