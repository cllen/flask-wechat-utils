#coding:utf8

#login
import logging
logging.basicConfig(level=logging.DEBUG)
_logger = logging.getLogger(__name__)

#wechat
from flask_wechat_utils import config as config_common

#database
from models import MessageTemplate

#utils
import requests

#error
from exceptions import ApplicationException
from exceptions import ERROR_MESSAGE_TEMPLATE_NOT_AUTH
from exceptions import ERROR_MESSAGE_TEMPLATE_SAVE_FORMID_MISSING_FORMID
from exceptions import ERROR_MESSAGE_TEMPLATE_GET_ACCESSTOKEN_ERROR
from exceptions import ERROR_MESSAGE_TEMPLATE_NO_FORMID

#----------------------------------
# api !!!
#----------------------------------
def save_formid(func):

	def wapper(self, *args, **kwargs):

		_logger.debug('-----------save_formid-------------')
		
		#need to auth before running to here
		if not hasattr(self,wechat_user):
			raise ApplicationException(
				errcode=ERROR_MESSAGE_TEMPLATE_NOT_AUTH,
			)

		form_id = request.json.get('form_id')

		if not form_id:
			raise ApplicationException(
				errcode=ERROR_MESSAGE_TEMPLATE_SAVE_FORMID_MISSING_FORMID,
			)

		message_template = MessageTemplate(
			openid=self.wechat_user.openid,
			form_id=args.get('form_id'),
		)

		message_template.save()

		return func(self, *args, **kwargs)

	return wapper


#----------------------------------
# api !!!
#----------------------------------

def send_message_template(touser,template_id,page=None,data=None,emphasis_keyword=None):

	_logger.debug('-----------send message template-------------')

	form_id_result = get_formid_and_delete(openid=touser)

	access_token = get_acecess_token()['access_token']

	url = "https://api.weixin.qq.com/cgi-bin/message/wxopen/template/send?" + \
		"access_token={}".format(access_token)

	data = {
		'touser':touser,
		'template_id':template_id,
		'form_id':form_id_result.form_id,
	}

	if page:
		data.update({'page':page})
	if data:
		data.update({'data':data})
	if emphasis_keyword:
		data.update({'emphasis_keyword':emphasis_keyword})

	response = requests.post(url,data=data)

	if response.json()['errcode'] in [40037,41028,41029,41030,45009]:
		_logger.debug(response.content)
		raise ApplicationException(
			errcode=ERROR_MESSAGE_TEMPLATE_GET_ACCESSTOKEN_ERROR,
		)
	else:
		_logger.debug(response.content)
		return True



def get_acecess_token():
	grant_type = 'client_credential'
	appid = config_common.WXAPP_ID
	secret = config_common.WXAPP_SECRET
	url = 'https://api.weixin.qq.com/cgi-bin/token?' + \
		'grant_type={}&appid={}&secret={}'.format(grant_type,appid,secret)

	response = requests.get(url)

	if response.json()['errcode'] == 0:
		return response.json()
	else:
		_logger.debug(response.content)
		raise ApplicationException(
			errcode=ERROR_MESSAGE_TEMPLATE_GET_ACCESSTOKEN_ERROR,
		)

def get_formid_and_delete(openid):

	try:
		form_id = MessageTemplate.objects(openid=openid).order_by('+created_ts').first()
	except:
		raise ApplicationException(
			errcode=ERROR_MESSAGE_TEMPLATE_NO_FORMID,
		)

	#delete
	#result_delete = MessageTemplate.objects(pk=form_id.pk).delete()

	return form_id

