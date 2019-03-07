#coding:utf8
from flask import Flask
import flask_wechat_utils
from flask_wechat_utils.user.utils import auth
from flask_wechat_utils.user.utils import login
from flask_wechat_utils.user.utils import register

app = Flask(__name__)

#-------------------------------------------
# 1 config app
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
app.config['WEB_NAME'] = 'myweb'
app.config['TEMPLATE_ID'] = None

#-------------------------------------------
# 2 init (db/bp/api)
#-------------------------------------------
flask_wechat_utils.init_app(app)


#-------------------------------------------
# 3 my routees
#-------------------------------------------
from flask_wechat_utils.config import api

ns = api.namespace(
	'myapplication', 
	description='descriptions of myapplication'
)

@ns.route('/user')
class User(Resource):

	@login
	def post(self):
		return {
			'code':0,
			'token':self.wechat_user_token,
		}

	@register
	def put(self):
		return {
			'code':0,
			'nickname':self.wechat_user.nickname,
			'avatar':self.wechat_user.avatar,
		}

	@auth
	def get(self):
		return {
			'code':0,
			'nickname':self.wechat_user.nickname,
			'avatar':self.wechat_user.avatar,
		}

#-------------------------------------------
# 3 flask-wechat-utils routes
#-------------------------------------------
# from flask_wechat_utils.user import routes				#使用默认user路由
# from flask_wechat_utils.message_template import routes	#使用默认message_template路由

if __name__ == '__main__':
	app.run(host='0.0.0.0',port=5000)

# post http://127.0.0.1:5000/myweb/user
# get http://127.0.0.1:5000/myweb/user
# put http://127.0.0.1:5000/myweb/user
