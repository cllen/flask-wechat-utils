#coding:utf8

#login
import logging
logging.basicConfig(level=logging.DEBUG)
_logger = logging.getLogger(__name__)

#frame
from flask_restplus import Resource

#wechat
from flask_wechat_utils import api
from flask_wechat_utils import utils as utils_common
import config as config_application

#model
from models import MessageTemplate

#application
from flask_wechat_utils.user.utils import auth
from utils import get_formid_and_delete


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


