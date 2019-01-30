#coding:utf8
from flask import Flask
import flask_wechat_utils

#-------------------------------------------
# app
#-------------------------------------------
app = Flask(__name__)

#-------------------------------------------
# config
#-------------------------------------------
app.config['MONGODB_SETTINGS'] = {
	'db': 'blog',
	'host': 'mongo',
	'port': 27017,
}

app.WXAPP_ID = 'xxx'
app.WXAPP_SECRET = 'xxx'
app.TOKEN_SECRET_KEY = 'xxx'
app.TOKEN_SALT = 'xxx'
app.TOKEN_TIMEOUT_HOURS = 24 * 365
app.WEB_NAME = 'zhihu'
app.TEMPLATE_ID = None

#-------------------------------------------
# config flask-wechat-utils (db/bp/api)
#-------------------------------------------
flask_wechat_utils.init_app(app)

#-------------------------------------------
# register bp
#-------------------------------------------
app.register_blueprint(flask_wechat_utils.config.bp)

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