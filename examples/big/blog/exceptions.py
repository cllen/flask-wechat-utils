#coding:utf8
from werkzeug.exceptions import HTTPException

ERROR_BLOG_EMPTY 			= 2001
ERROR_WRONG_BLOG_ID			= 2002

ERROR_MSG = {
	ERROR_BLOG_EMPTY: {
		'message': 'blog empty',
		'http_code': 400,
		'sub_category': 'blog',
	},
	ERROR_WRONG_BLOG_ID: {
		'message': 'wrong blog id',
		'http_code': 400,
		'sub_category': 'blog',
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

	category = 'myweb.blog'

	co_msg_mapping = ERROR_MSG