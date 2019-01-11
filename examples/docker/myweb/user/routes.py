#coding:utf8
import logging
logging.basicConfig(level=logging.DEBUG)
_logger = logging.getLogger(__name__)

#frame
from flask_restplus import Resource, fields, Api
from flask import Blueprint

#flask_wechat_utils
from flask_wechat_utils.auth import config
from flask_wechat_utils.utils import now_ts
from flask_wechat_utils.auth import login
from flask_wechat_utils.auth import register
from flask_wechat_utils.auth import auth
from flask_wechat_utils.auth import get_web_name

#model
from flask_wechat_utils.models import User


#-------------------------------------------
# get app config
#-------------------------------------------
web_name = get_web_name()

#-------------------------------------------
# blueprint/api/ns
#-------------------------------------------
bp = Blueprint(
	config.APPLICATION_NAME, 
	__name__, 
	url_prefix='/{}'.format(web_name)
)
api = Api(
	bp, 
	version=config.APPLICATION_VERSION, 
	title='{} API'.format(web_name),
	description=config.APPLICATION_DESCRIPTION,
)
ns = api.namespace(
	config.APPLICATION_NAME, 
	description=config.APPLICATION_DESCRIPTION
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
@ns.route('/user')
class UserRoute(Resource):

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


@ns.route('/test')
class Test(Resource):

	@api.marshal_with(marshal_user_register)
	@auth
	def get(self):

		return {
			'code':0,
			'user':self.wechat_user,
		}
