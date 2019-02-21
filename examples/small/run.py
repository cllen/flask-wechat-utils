#coding:utf8
from flask import Flask
import flask_wechat_utils

app = Flask(__name__)

#-------------------------------------------
# config app
#-------------------------------------------
app.config['MONGODB_SETTINGS'] = {
	'db': 'xxx',
	'host': '127.0.0.1',
	'port': 27017,
}

app.config['WXAPP_ID'] = 'xxx'
app.config['WXAPP_SECRET'] = 'xxx'
app.config['TOKEN_SECRET_KEY'] = 'xxx'
app.config['TOKEN_SALT'] = 'xxx'
app.config['TOKEN_TIMEOUT_HOURS'] = 24 * 365
app.config['WEB_NAME'] = 'xxx'
app.config['TEMPLATE_ID'] = None

#-------------------------------------------
# config flask-wechat-utils (db/bp/api)
#-------------------------------------------
flask_wechat_utils.init_app(app)

#-------------------------------------------
# register bp
#-------------------------------------------
app.register_blueprint(flask_wechat_utils.config.bp)

#-------------------------------------------
# my routees
#-------------------------------------------
from flask_wechat_utils.config import api
ns = api.namespace(
	'myapplication', 
	description='descriptions of myapplication'
)

@ns.route('/test')	# http://127.0.0.1:5000/myweb/myapplication/test
class AuthRoute(Resource):

	@auth
	def get(self):

		return {
			'code':0,
			'nickname':self.wechat_user.nickname,
			'avatar':self.wechat_user.avatar,
		}

#-------------------------------------------
# flask-wechat-utils routes
#-------------------------------------------
from flask_wechat_utils.user import routes				#使用默认user路由
from flask_wechat_utils.message_template import routes	#使用默认message_template路由

if __name__ == '__main__':
	app.run(host='0.0.0.0',port=5000)