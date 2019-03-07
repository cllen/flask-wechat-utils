#coding:utf8

#login
import logging
logging.basicConfig(level=logging.DEBUG)
_logger = logging.getLogger(__name__)

#flask frame
from flask_restplus import Resource, fields

#wechat frame
import flask_wechat_utils
from flask_wechat_utils.config import api
import config as config_application

#application models
from models import User

#application utils
from utils import login
from utils import register
from utils import auth

#-------------------------------------------
# namespace
#-------------------------------------------
ns = api.namespace(
	config_application.APPLICATION_NAME, 
	description=config_application.APPLICATION_DESCRIPTION
)

#-------------------------------------------
# /parser/marshal
#-------------------------------------------

parser_user_register = api.parser()
parser_user_register.add_argument('nickname')
parser_user_register.add_argument('avatar')
parser_user_register.add_argument('gender')
parser_user_register.add_argument('city')
parser_user_register.add_argument('province')
parser_user_register.add_argument('country')
parser_user_register.add_argument('language')
parser_user_register.add_argument('encryptedData')
parser_user_register.add_argument('iv')
parser_user_register.add_argument('code')

parser_user_login = api.parser()
parser_user_login.add_argument('code')

# marshal base user
marshal_user_base = api.model(
	'marshal_user_detail', 
	{
		'nickname': fields.String(required=True, description='the nickname of user'),
		'avatar': fields.String(required=True, description='The avatar of user'),
		'gender': fields.String(required=True, description='The gender of user'),
		'city': fields.String(required=True, description='The city of user'),
		'province': fields.String(required=True, description='province id of user'),
		'country': fields.String(required=True, description='The country of user'),
		'language': fields.String(required=True, description='The language of user'),
	},
)

marshal_user_register = api.model(
	'marshal_user_login', 
	{
		'code': fields.Integer(description='server code'),
		'user': fields.Nested(marshal_user_base)
	},
)

marshal_user_login = api.model(
	'marshal_user_login', 
	{	
		'code': fields.Integer(description='server code'),
		'token': fields.String(required=True, description='The id of book'),
	},
)

#-------------------------------------------
# route
#-------------------------------------------
#@api.doc(responses={404: 'some params is not found'}, params={'som_params': 'the params of this api'})
@ns.route('/user')
class User(Resource):

	@api.doc(parser=parser_user_login)
	@api.marshal_with(marshal_user_login)
	@login
	def post(self):
		return {
			'code':0,
			'token':self.wechat_user_token,
		}

	@api.doc(parser=parser_user_register)
	@api.marshal_with(marshal_user_register)
	@register
	def put(self):
		return {
			'code':0,
			'user':self.wechat_user,
		}

	@api.marshal_with(marshal_user_register)
	@auth
	def get(self):

		return {
			'code':0,
			'user':self.wechat_user,
		}

