#coding:utf8

#frame
from werkzeug.exceptions import HTTPException

ERROR_MESSAGE_TEMPLATE_NOT_AUTH						=	1301
ERROR_MESSAGE_TEMPLATE_SAVE_FORMID_MISSING_FORMID	=	1302
ERROR_MESSAGE_TEMPLATE_GET_ACCESSTOKEN_ERROR		=	1303
ERROR_MESSAGE_TEMPLATE_NO_FORMID 					=	1304
ERROR_MESSAGE_TEMPLATE_TEMPLATE_ID_IS_NONE 			=	1305

ERROR_MSG = {
	ERROR_MESSAGE_TEMPLATE_TEMPLATE_ID_IS_NONE: {
		'message': 'TEMPLATE_ID is None, please configure message_template.config.TEMPLATE_ID',
		'http_code': 500,
		'sub_category': 'wechat.message_template',
	},
	ERROR_MESSAGE_TEMPLATE_GET_ACCESSTOKEN_ERROR: {
		'message': 'get access token error',
		'http_code': 400,
		'sub_category': 'wechat.message_template',
	},
	ERROR_MESSAGE_TEMPLATE_NO_FORMID: {
		'message': 'this user has no formid in database',
		'http_code': 400,
		'sub_category': 'wechat.message_template',
	},
	ERROR_MESSAGE_TEMPLATE_NOT_AUTH: {
		'message': 'please use @auth before @get_formid',
		'http_code': 400,
		'sub_category': 'wechat.message_template',
	},
	ERROR_MESSAGE_TEMPLATE_SAVE_FORMID_MISSING_FORMID: {
		'message': 'missing form_id',
		'http_code': 400,
		'sub_category': 'wechat.message_template',
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

	category = 'wechat.message_template'

	co_msg_mapping = ERROR_MSG