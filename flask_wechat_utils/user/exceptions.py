#coding:utf8

#frame
from werkzeug.exceptions import HTTPException

#error 						  	登录10:01错误位置
ERROR_TOKEN_MISSING 			= 1001
ERROR_TOKEN_WRONG_DECRYPT		= 1002
ERROR_TOKEN_TIMEOUT				= 1003
ERROR_TOKEN_WRONG_FIELDS		= 1004
ERROR_TOKEN_WRONG_NO_USER		= 1005
ERROR_CODE_WRONG				= 1006
ERROR_IV_ENCRYPTED_WRONG 		= 1007
ERROR_MONGO_GET_USER_WRONG		= 1008
ERROR_TOKEN_WRONG_ENCRYPT		= 1009
ERROR_CONTENT_TYPE_NOT_JSON		= 1010

ERROR_LOGIN_CODE_MISSING				= 1101
ERROR_LOGIN_CODE_FREQUENCY_LIMIT		= 1102
ERROR_LOGIN_CODE_WEIXIN_BUSY			= 1103
ERROR_LOGIN_CODE_LOST_EFFECT			= 1104
ERROR_LOGIN_CODE_NO_WHY					= 1105
ERROR_LOGIN_MONGO_CREATE_FAIL			= 1106
ERROR_LOGIN_MONGO_UPDATE_FAIL			= 1107
ERROR_REGISTER_MISSING_IV_OR_ENCRYPTED	= 1108
ERROR_REGISTER_MISSING_TOKEN			= 1109
ERROR_REGISTER_NO_USER					= 1110

ERROR_MISSING_WXAPP_ID				= 1200
ERROR_MISSING_WXAPP_SECRET			= 1201

ERROR_CONFIG_WEB_NAME_WRONG								= 1202
ERROR_CONFIG_TOKEN_SECRET_KEY_WRONG						= 1203
ERROR_CONFIG_TOKEN_TIMEOUT_HOURS_WRONG					= 1204
ERROR_CONFIG_TOKEN_SALT_WRONG							= 1205
ERROR_CONFIG_TOKEN_FIELDS_REQUIRED_WRONG				= 1206
ERROR_CONFIG_TOKEN_HEADER_FIELD_WRONG					= 1207
ERROR_CONFIG_LOGIN_CODE_FIELD_NAME_WRONG				= 1208
ERROR_CONFIG_UPDATE_IV_FIELD_NAME_WRONG					= 1209
ERROR_CONFIG_UPDATE_ENCRYPTEDDATA_FIELD_NAME_WRONG		= 1210

ERROR_MSG = {
	ERROR_CONTENT_TYPE_NOT_JSON: {
		'message': 'please add to the headers: applcation:content/json',
		'http_code': 400,
		'sub_category': 'wechat',
	},

	ERROR_MISSING_WXAPP_ID: {
		'message': 'missing WXAPP_ID',
		'http_code': 500,
		'sub_category': 'wechat',
	},
	ERROR_MISSING_WXAPP_SECRET: {
		'message': 'missing WXAPP_SECRET',
		'http_code': 500,
		'sub_category': 'wechat',
	},
	ERROR_CONFIG_TOKEN_SECRET_KEY_WRONG: {
		'message': 'config TOKEN_SECRET_KEY wrong!',
		'http_code': 500,
		'sub_category': 'wechat',
	},
	ERROR_CONFIG_WEB_NAME_WRONG: {
		'message': 'config WEB_NAME wrong!',
		'http_code': 500,
		'sub_category': 'wechat',
	},
	ERROR_CONFIG_TOKEN_TIMEOUT_HOURS_WRONG: {
		'message': 'config TOKEN_TIMEOUT_HOURS wrong!',
		'http_code': 500,
		'sub_category': 'wechat',
	},
	ERROR_CONFIG_TOKEN_SALT_WRONG: {
		'message': 'config TOKEN_SALT wrong!',
		'http_code': 500,
		'sub_category': 'wechat',
	},
	ERROR_CONFIG_TOKEN_FIELDS_REQUIRED_WRONG: {
		'message': 'config TOKEN_FIELDS_REQUIRED wrong!',
		'http_code': 500,
		'sub_category': 'wechat',
	},
	ERROR_CONFIG_TOKEN_HEADER_FIELD_WRONG: {
		'message': 'config TOKEN_HEADER_FIELD wrong!',
		'http_code': 500,
		'sub_category': 'wechat',
	},
	ERROR_CONFIG_LOGIN_CODE_FIELD_NAME_WRONG: {
		'message': 'config CODE_LOGIN_FIELD_NAME wrong!',
		'http_code': 500,
		'sub_category': 'wechat',
	},
	ERROR_CONFIG_UPDATE_IV_FIELD_NAME_WRONG: {
		'message': 'config UPDATE_IV_FIELD_NAME wrong!',
		'http_code': 500,
		'sub_category': 'wechat',
	},
	ERROR_CONFIG_UPDATE_ENCRYPTEDDATA_FIELD_NAME_WRONG: {
		'message': 'config UPDATE_ENCRYPTEDDATA_FIELD_NAME wrong!',
		'http_code': 500,
		'sub_category': 'wechat',
	},


	ERROR_LOGIN_CODE_MISSING: {
		'message': 'missing code,or chat that you are posting json-type data?',
		'http_code': 400,
		'sub_category': 'wechat.auth.login',
	},
	ERROR_LOGIN_CODE_FREQUENCY_LIMIT: {
		'message': 'frequency limit',
		'http_code': 400,
		'sub_category': 'wechat.auth.login',
	},
	ERROR_LOGIN_CODE_WEIXIN_BUSY: {
		'message': 'weixin busy',
		'http_code': 400,
		'sub_category': 'wechat.auth.login',
	},
	ERROR_LOGIN_CODE_LOST_EFFECT: {
		'message': 'lost effect',
		'http_code': 400,
		'sub_category': 'wechat.auth.login',
	},
	ERROR_LOGIN_CODE_NO_WHY: {
		'message': 'weixin said that no why,failure is failure',
		'http_code': 400,
		'sub_category': 'wechat.auth.login',
	},
	ERROR_LOGIN_MONGO_CREATE_FAIL: {
		'message': 'mongo create user wrong',
		'http_code': 500,
		'sub_category': 'wechat.auth.login',
	},
	ERROR_LOGIN_MONGO_UPDATE_FAIL: {
		'message': 'mongo update user wrong',
		'http_code': 500,
		'sub_category': 'wechat.auth.login',
	},
	ERROR_REGISTER_MISSING_IV_OR_ENCRYPTED: {
		'message': 'register missing iv or encrypted,or chat that you are putting json-type data?',
		'http_code': 400,
		'sub_category': 'wechat.auth.login',
	},
	ERROR_REGISTER_MISSING_TOKEN: {
		'message': 'register missing token',
		'http_code': 500,
		'sub_category': 'wechat.auth.login',
	},


	ERROR_TOKEN_MISSING: {
		'message': 'missing token',
		'http_code': 400,
		'sub_category': 'wechat.auth.auth',
	},
	ERROR_TOKEN_WRONG_DECRYPT: {
		'message': 'token wrong,decrypt fail!',
		'http_code': 400,
		'sub_category': 'wechat.auth.auth',
	},
	ERROR_TOKEN_TIMEOUT: {
		'message': 'token timeout!',
		'http_code': 400,
		'sub_category': 'wechat.auth.auth',
	},
	ERROR_TOKEN_WRONG_FIELDS: {
		'message': 'token wrong fields!',
		'http_code': 400,
		'sub_category': 'wechat.auth.auth',
	},
	ERROR_TOKEN_WRONG_NO_USER: {
		'message': 'token wrong,no user!check your tokens user whether or not that its existed',
		'http_code': 400,
		'sub_category': 'wechat.auth.auth',
	},
	ERROR_CODE_WRONG: {
		'message': 'code wrong!',
		'http_code': 400,
		'sub_category': 'wechat.auth.auth',
	},
	ERROR_IV_ENCRYPTED_WRONG: {
		'message': 'iv and encrypted wrong!',
		'http_code': 400,
		'sub_category': 'wechat.auth.auth',
	},

	ERROR_MONGO_GET_USER_WRONG: {
		'message': 'mongo get user wrong!,check your mmongo config',
		'http_code': 500,
		'sub_category': 'wechat.auth.auth',
	},

	ERROR_LOGIN_CODE_MISSING: {
		'message': 'missing code',
		'http_code': 400,
		'sub_category': 'wechat.auth.login',
	},

	ERROR_LOGIN_CODE_MISSING: {
		'message': 'missing code',
		'http_code': 400,
		'sub_category': 'wechat.auth.login',
	},
	ERROR_TOKEN_WRONG_ENCRYPT: {
		'message': 'token encrypt fail',
		'http_code': 400,
		'sub_category': 'wechat.auth.login',
	},
	ERROR_REGISTER_MISSING_TOKEN: {
		'message': 'missing token',
		'http_code': 400,
		'sub_category': 'wechat.auth.register',
	},
	ERROR_REGISTER_NO_USER: {
		'message': 'database have no this user',
		'http_code': 400,
		'sub_category': 'wechat.auth.register',
	},
}

class BaseAppException(HTTPException):
	category = None
	co_msg_mapping = {}

	def __init__(self, errcode, message=None, sub_category=None, params=None,
			http_code=None, description=None, return_data=None):
		co_info = self.co_msg_mapping.get(errcode, {})
		if message is None:
			message = co_info.get('message')
		if description is None:
			description = co_info.get('description')
		if http_code is None:
			http_code = co_info.get('http_code')
		if sub_category is None:
			sub_category = co_info.get('sub_category')

		super(BaseAppException,self).__init__(description=description)

		self.code = http_code
		self.errcode = errcode
		self.message = message

		self.sub_category = sub_category
		self.params = params
		self.data = {
			'message': self.message,
			'errcode': self.errcode,
			'category': self.category,
			'sub_category': self.sub_category,
		}

		if return_data is None:
			return_data = {}
		self.return_data = return_data
		if return_data is not None and isinstance(return_data, dict):
			self.data.update(data=return_data)

		if params is not None and isinstance(params, dict):
			self.data.update(params=params)

	def __repr__(self):
		return '{}: category: {}; sub_category: {}; errcode: {}; message: {}; data: {}'.format(
			self.__class__.__name__,
			self.category,
			self.sub_category,
			self.errcode,
			self.message,
			self.data,
		)


class ApplicationException(BaseAppException):

	category = 'wechat.auth'

	co_msg_mapping = ERROR_MSG





# from flask import Flask, request, json

# def test():
# 	raise MyException(error_code=ERROR_TOKEN_WRONG_DECRYPT)

# app = Flask(__name__)

# @app.route('/')
# def hello_world():
# 	#test()
# 	raise InvalidUsage('This view is gone', status_code=410)


# @app.errorhandler(InvalidUsage)
# def handle_invalid_usage(error):
# 	response = jsonify(error.to_dict())
# 	response.status_code = error.status_code
# 	return response


# if __name__ == '__main__':
# 	app.run()





