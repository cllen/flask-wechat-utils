#coding:utf8

#login
import logging
logging.basicConfig(level=logging.DEBUG)
_logger = logging.getLogger(__name__)

#frame
from flask_restplus import Resource

#wechat
from flask_wechat_utils.config import api
from flask_wechat_utils.user.utils import auth
from flask_wechat_utils.message_template.utils import save_formid
from flask_wechat_utils.message_template.utils import send_message_template

#model
from flask_wechat_utils.message_template.models import MessageTemplate

#application
import config as config_application

#error
from flask_wechat_utils.message_template.exceptions import ApplicationException
from flask_wechat_utils.message_template.exceptions import ERROR_MESSAGE_TEMPLATE_TEMPLATE_ID_IS_NONE

#-------------------------------------------
# blueprint/api/ns
#-------------------------------------------
ns = api.namespace(
	config_application.APPLICATION_NAME, 
	description=config_application.APPLICATION_DESCRIPTION
)


#-------------------------------------------
# /parser/marshal
#-------------------------------------------
parser_messageTemplate_create = api.parser()
parser_messageTemplate_create.add_argument('form_id',type=str,required=True)


#-------------------------------------------
# route
#-------------------------------------------
@ns.route('/save_formid')
class MessageTemplateSaveRoute(Resource):

	#将用户formid写入数据库
	@api.doc(parser=parser_messageTemplate_create)
	@auth
	@save_formid
	def post(self):
		return {
			'code':0,
		}

@ns.route('/send_message')
class MessageTemplateSendRoute(Resource):

	#发送message
	@auth
	def post(self):

		if config_application.TEMPLATE_ID == None:
			raise ApplicationException(
				errcode=ERROR_MESSAGE_TEMPLATE_TEMPLATE_ID_IS_NONE,
			)

		send_message_template(
			touser=self.wechat_user.openid,
			template_id=config.TEMPLATE_ID,
			page=None,
			data=None,
			emphasis_keyword=None
		)

		return {
			'code':0,
		}


