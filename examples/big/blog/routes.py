#coding:utf8

#log
import logging
logging.basicConfig(level=logging.DEBUG)
_logger = logging.getLogger(__name__)

#frame
from flask_restplus import Resource, fields
from flask import Blueprint

# wechat
from flask_wechat_utils import api
from flask_wechat_utils.user.utils import auth
from flask_wechat_utils.utils import now_ts

# applicaton
import config as config_application

#model
from models import Blog

#error
from exceptions import ERROR_BLOG_EMPTY
from exceptions import ERROR_WRONG_BLOG_ID
from exceptions import ApplicationException

#-------------------------------------------
# get app config
#-------------------------------------------
application_name = config_application.APPLICATION_NAME
application_description = config_application.APPLICATION_DESCRIPTION

#-------------------------------------------
# blueprint/api/ns
#-------------------------------------------
ns = api.namespace(
	application_name, 
	description=application_description
)

#-------------------------------------------
# /parser/marshal
#-------------------------------------------
#detail
parser_blog_detail = api.parser()
parser_blog_detail.add_argument('blogid',type=str,required=True)

#create
parser_blog_create = api.parser()
parser_blog_create.add_argument('text',type=str,required=True)

#list
parser_blog_list = api.parser()
parser_blog_list.add_argument('page',type=int,default=0)
parser_blog_list.add_argument('num',type=int,default=10)

#base
marshal_user_detail_base = api.model(
	'marshal_user_detail', 
	{
		'nickname': fields.String(description='the nickname of user'),
		'avatar': fields.String(description='The avatar of user'),
	},
)

marshal_blog_detail_base = api.model(
	'marshal_blog_detail_base', 
	{
		'text': fields.String(description='The text of blog'),
		'created_ts': fields.Integer(description='The created_ts of blog'),
	},
)

#detail
marshal_blog_detail = api.model(
	'marshal_blog_detail', 
	{
		'code': fields.Integer(description='server code'),
		'user':fields.Nested(marshal_user_detail_base),
		'blog':fields.Nested(marshal_blog_detail_base)
	},
)

#list
marshal_blog_list = api.model(
	'marshal_blog_list', 
	{	
		'code': fields.Integer(description='server code'),
		'user':fields.Nested(marshal_user_detail_base),
		'blogs': fields.List(fields.Nested(marshal_blog_detail_base))
	},
)

#-------------------------------------------
# route
#-------------------------------------------
@ns.route('/detail')
class BlogDetail(Resource):

	@api.doc(parser=parser_blog_detail)
	@api.marshal_with(marshal_blog_detail)
	@auth
	def get(self):

		args = parser_blog_detail.parse_args()

		try:
			blog = Blog.objects.get_or_404(pk=args.get('blogid'))
		except:
			raise ApplicationException(
				errcode=ERROR_WRONG_BLOG_ID,
			)

		return {
			'code':0,
			'user':self.wechat_user,
			'blog':blog,
		}

	@api.doc(parser=parser_blog_create)
	@api.marshal_with(marshal_blog_detail)
	@auth
	def post(self):

		args = parser_blog_create.parse_args()

		result = Blog(
			openid=self.wechat_user.openid,
			text=args.get('text'),
			created_ts=now_ts()
		)

		result.save()

		blog = Blog.objects.get(pk=result.pk)

		if result:
			return {
				'code':0,
				'user':self.wechat_user,
				'blog':blog,
			}
		else:
			return {
				'code':-1,
			}

@ns.route('/list')
class BlogList(Resource):
	@api.doc(parser=parser_blog_list)
	@api.marshal_with(marshal_blog_list)
	@auth
	def get(self):

		args = parser_blog_list.parse_args()

		try:
			blogs = Blog.objects.paginate(page=args['page'],per_page=args['num'])
		except:
			raise ApplicationException(
				errcode=ERROR_BLOG_EMPTY,
			)

		return {
			'code':0,
			'user':self.wechat_user,
			'blogs':blogs,
		}

