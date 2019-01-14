#coding:utf8
from flask import Flask

from flask_wechat_utils import bp as wechat_bp
from flask_wechat_utils import db as wechat_db
from flask_wechat_utils import config as wechat_config
from flask_wechat_utils.message_template import config as message_template_config

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
message_template_config.TEMPLATE_ID = None

#-------------------------------------------
# 固定写法，不需要修改，初始化数据库+注册路由
#-------------------------------------------
wechat_db.init_app(app)
app.register_blueprint(wechat_bp)

#-------------------------------------------
# 用户自定义路由
#-------------------------------------------
#from flask_wechat_utils.user import routes				#login,register,auth，是本库的路由
#from flask_wechat_utils.message_template import routes	#template_message，是本库的路由

from user import routes									#login,register,auth，是开发者自定义的路由
from blog import routes									#blog，是开发者自定义的路由
from message_template import routes						#message_template，是开发者自定义的路由


if __name__ == '__main__':
	app.run(host='0.0.0.0',port=5000)