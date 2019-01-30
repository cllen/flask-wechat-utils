#coding:utf8

#login
import logging
logging.basicConfig(level=logging.DEBUG)
_logger = logging.getLogger(__name__)

#flask frame
from flask_restplus import Resource

#wechat frame
import flask_wechat_utils
from flask_wechat_utils.user.utils import auth
from flask_wechat_utils.config import api

#application config
import config as config_application

#application model
from models import MessageTemplate

#application
from utils import get_formid_and_delete

#-------------------------------------------
# blueprint/api/ns
#-------------------------------------------
ns = api.namespace(
	config_application.APPLICATION_NAME, 
	description=config_application.APPLICATION_DESCRIPTION
)

# api = flask_wechat_utils.create_api()

# ns = api.namespace(
# 	config_application.APPLICATION_NAME, 
# 	description=config_application.APPLICATION_DESCRIPTION
# )

#-------------------------------------------
# /parser/marshal
#-------------------------------------------
parser_messageTemplate_create = api.parser()
parser_messageTemplate_create.add_argument('form_id',type=str,required=True)

#-------------------------------------------
# route
#-------------------------------------------
@ns.route('/')
class MessageTemplateRoute(Resource):

	@api.doc(parser=parser_messageTemplate_create)
	@auth
	def post(self):

		args = parser_messageTemplate_create.parse_args()

		message_template = MessageTemplate(
			openid=self.wechat_user.openid,
			form_id=args.get('form_id'),
		)

		message_template.save()

		return {
			'code':0,
		}

	@auth
	def get(self):

		form_id_result = get_formid_and_delete(self.wechat_user.openid)

		return {
			'code':0,
			'openid':form_id_result.openid,
			'created_ts':str(form_id_result.created_ts),
			'_id':str(form_id_result.id),
		}


