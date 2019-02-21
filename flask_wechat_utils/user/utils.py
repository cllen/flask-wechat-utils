#coding:utf8
import logging
logging.basicConfig(level=logging.DEBUG)
_logger = logging.getLogger(__name__)

#exception
from exceptions import ApplicationException

#crypt
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from itsdangerous import SignatureExpired
import base64
import json
import traceback
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.padding import PKCS7

#common
import time
from pprint import pprint
from flask import request
import logging
import requests
from flask_wechat_utils.utils import now_ts

#database
from flask_wechat_utils import config as config_common
from models import User


#error
from exceptions import ERROR_TOKEN_MISSING
from exceptions import ERROR_TOKEN_WRONG_DECRYPT
from exceptions import ERROR_TOKEN_TIMEOUT
from exceptions import ERROR_TOKEN_WRONG_FIELDS
from exceptions import ERROR_TOKEN_WRONG_NO_USER
from exceptions import ERROR_CODE_WRONG
from exceptions import ERROR_IV_ENCRYPTED_WRONG
from exceptions import ERROR_MONGO_GET_USER_WRONG
from exceptions import ERROR_TOKEN_WRONG_ENCRYPT
from exceptions import ERROR_CONTENT_TYPE_NOT_JSON

from exceptions import ERROR_LOGIN_CODE_MISSING
from exceptions import ERROR_LOGIN_CODE_FREQUENCY_LIMIT
from exceptions import ERROR_LOGIN_CODE_WEIXIN_BUSY
from exceptions import ERROR_LOGIN_CODE_LOST_EFFECT
from exceptions import ERROR_LOGIN_CODE_NO_WHY
from exceptions import ERROR_LOGIN_MONGO_CREATE_FAIL
from exceptions import ERROR_LOGIN_MONGO_UPDATE_FAIL

from exceptions import ERROR_REGISTER_MISSING_IV_OR_ENCRYPTED
from exceptions import ERROR_REGISTER_MISSING_TOKEN
from exceptions import ERROR_REGISTER_NO_USER

from exceptions import ERROR_MISSING_WXAPP_ID
from exceptions import ERROR_MISSING_WXAPP_SECRET

from exceptions import ERROR_CONFIG_WEB_NAME_WRONG
from exceptions import ERROR_CONFIG_TOKEN_SECRET_KEY_WRONG
from exceptions import ERROR_CONFIG_TOKEN_TIMEOUT_HOURS_WRONG
from exceptions import ERROR_CONFIG_TOKEN_SALT_WRONG
from exceptions import ERROR_CONFIG_TOKEN_FIELDS_REQUIRED_WRONG
from exceptions import ERROR_CONFIG_TOKEN_HEADER_FIELD_WRONG
from exceptions import ERROR_CONFIG_LOGIN_CODE_FIELD_NAME_WRONG
from exceptions import ERROR_CONFIG_UPDATE_IV_FIELD_NAME_WRONG
from exceptions import ERROR_CONFIG_UPDATE_ENCRYPTEDDATA_FIELD_NAME_WRONG


#----------------------------------
# auth api !!!
#----------------------------------
def auth(func):

	def wapper(self, *args, **kwargs):

		_logger.debug('-----------user authing-------------')
		
		token = request.environ.get('HTTP_{}'.format(get_token_header_field().upper()))
		content_type = request.environ.get('CONTENT_TYPE')

		_logger.debug({'content_type':content_type,'token':token})

		if not content_type or not content_type.lower() == 'application/json':
			raise ApplicationException(
				errcode=ERROR_CONTENT_TYPE_NOT_JSON,
			)

		if not token:
			raise ApplicationException(
				errcode=ERROR_TOKEN_MISSING,
			)
		else:
			self.wechat_user = get_wechat_user_info_from_database(token)

		return func(self, *args, **kwargs)

	return wapper


#----------------------------------
# user login api !!!
#----------------------------------
def login(func):

	def wapper(self, *args, **kwargs):

		_logger.debug('-----------user logining------------')

		content_type = request.environ.get('CONTENT_TYPE')

		if not content_type or not content_type.lower() == 'application/json':
			raise ApplicationException(
				errcode=ERROR_CONTENT_TYPE_NOT_JSON,
			)

		code_field_name = get_login_code_field_name()

		#params = request.form
		params = request.json

		code = params.get(code_field_name)

		_logger.debug({'content_type':content_type,'code':code})

		if not code:
			raise ApplicationException(
				errcode=ERROR_LOGIN_CODE_MISSING,
			)

		result_login = get_session_key_from_weixin(
			appid=get_appid(),
			appsecret=get_appsecret(),
			js_code=params.get(code_field_name)
		)

		#success
		if result_login.get('session_key') and result_login.get('openid'):

			try:
				user = User.objects.get(openid=result_login['openid'])
			except:
				user = None

			#create
			if not user:
				try:
					User(
						session_key=result_login['session_key'],
						openid=result_login['openid'],
						last_login_ts=now_ts()
					).save()
				except:
					raise ApplicationException(
						errcode=ERROR_LOGIN_MONGO_CREATE_FAIL,
					)
			#update
			else:
				try:
					User.objects(openid=result_login['openid']).update_one(
						session_key=result_login['session_key'],
						last_login_ts=now_ts()
					)
				except:
					raise ApplicationException(
						errcode=ERROR_LOGIN_MONGO_UPDATE_FAIL,
					)

			user = User.objects.get(openid=result_login['openid'])

			userinfo = {}

			for key in get_token_fields_required():
				value = getattr(user,key)
				userinfo[key] = value

			self.wechat_user_token = encrypt_token(userinfo)

			self.wechat_user = user
		# #fail
		# elif result_login.get('errcode') == 45011:
		# 	raise ApplicationException(
		# 		errcode=ERROR_LOGIN_CODE_FREQUENCY_LIMIT,
		# 	)
		# elif result_login.get('errcode') == -1:
		# 	raise ApplicationException(
		# 		errcode=ERROR_LOGIN_CODE_WEIXIN_BUSY,
		# 	)
		# elif result_login.get('errcode') == 40029:
		# 	raise ApplicationException(
		# 		errcode=ERROR_LOGIN_CODE_LOST_EFFECT,
		# 	)
		else:
			_logger.debug(result_login)
			raise ApplicationException(
				errcode=ERROR_LOGIN_CODE_NO_WHY,
			)

		return func(self, *args, **kwargs)

	return wapper

#----------------------------------
# user update api !!!
#----------------------------------
def register(func):

	def wapper(self, *args, **kwargs):

		_logger.debug('-----------user registing-----------')

		token = request.environ.get('HTTP_{}'.format(get_token_header_field().upper()))
		content_type = request.environ.get('CONTENT_TYPE')

		_logger.debug({'content_type':content_type,'token':token})

		if not content_type or not content_type.lower() == 'application/json':
			raise ApplicationException(
				errcode=ERROR_CONTENT_TYPE_NOT_JSON,
			)

		if not token:
			raise ApplicationException(
				errcode=ERROR_REGISTER_MISSING_TOKEN,
			)

		#params = request.form
		params = request.json

		_logger.debug(params)

		encryptedData_field_name = get_update_encryptedData_field_name()

		iv_field_name = get_update_iv_field_name()

		if not params.get(iv_field_name) or not params.get(encryptedData_field_name):
			raise ApplicationException(
				errcode=ERROR_REGISTER_MISSING_IV_OR_ENCRYPTED,
			)

		iv = params.get(iv_field_name)

		encryptedData = params.get(encryptedData_field_name)

		result_token = decrypt_token(token)
		openid = result_token['openid']

		try:
			user = User.objects.get(openid=openid)
		except:
			raise ApplicationException(
				errcode=ERROR_REGISTER_MISSING_IV_OR_ENCRYPTED,
			)

		session_key = user.session_key
		#session_key = 'HKUOhvaNYvMxGCt2BpjfJg=='

		result_userinfo = decrypt(
			session_key = session_key,
			iv=iv,
			encrypted=encryptedData
		)

		user = User.objects(openid=user.openid).update_one(
			session_key=session_key,
			nickname=result_userinfo.get('nickName'),
			avatar=result_userinfo.get('avatarUrl'),
			gender=result_userinfo.get('gender'),
			city=result_userinfo.get('city'),
			province=result_userinfo.get('province'),
			country=result_userinfo.get('country'),
			language=result_userinfo.get('language'),
			mobile=result_userinfo.get('mobile'),
			last_login_ts=now_ts()
		)

		user = User.objects.get(openid=openid)

		self.wechat_user = user

		return func(self, *args, **kwargs)

	return wapper

#----------------------------------
# auth config
# configure it please if you replace "config" with something else
#----------------------------------
def get_appid():
	#return config_common.WXAPP_ID
	if not config_common.WXAPP_ID:
		raise ApplicationException(
			errcode=ERROR_MISSING_WXAPP_ID,
		)
	return config_common.WXAPP_ID

def get_appsecret():
	if not config_common.WXAPP_SECRET:
		raise ApplicationException(
			errcode=ERROR_MISSING_WXAPP_SECRET,
		)
	return config_common.WXAPP_SECRET

def get_web_name():
	if not isinstance(config_common.WEB_NAME, str):
		raise ApplicationException(
			errcode=ERROR_CONFIG_WEB_NAME_WRONG,
		)
	return config_common.WEB_NAME

def get_token_secret_key():
	if not isinstance(config_common.TOKEN_SECRET_KEY, str):
		raise ApplicationException(
			errcode=ERROR_CONFIG_TOKEN_SECRET_KEY_WRONG,
		)
	return config_common.TOKEN_SECRET_KEY

def get_token_timeout_hours():
	if not isinstance(config_common.TOKEN_TIMEOUT_HOURS, int):
		raise ApplicationException(
			errcode=ERROR_CONFIG_TOKEN_TIMEOUT_HOURS_WRONG,
		)
	return config_common.TOKEN_TIMEOUT_HOURS

def get_token_salt():
	if not isinstance(config_common.TOKEN_SALT, str):
		raise ApplicationException(
			errcode=ERROR_CONFIG_TOKEN_SALT_WRONG,
		)
	return config_common.TOKEN_SALT

def get_token_fields_required():
	if not isinstance(config_common.TOKEN_FIELDS_REQUIRED, list):
		raise ApplicationException(
			errcode=ERROR_CONFIG_TOKEN_FIELDS_REQUIRED_WRONG,
		)
	return config_common.TOKEN_FIELDS_REQUIRED

def get_token_header_field():
	if not isinstance(config_common.TOKEN_HEADER_FIELD, str):
		raise ApplicationException(
			errcode=ERROR_CONFIG_TOKEN_HEADER_FIELD_WRONG,
		)
	return config_common.TOKEN_HEADER_FIELD

def get_login_code_field_name():
	if not isinstance(config_common.LOGIN_CODE_FIELD_NAME, str):
		raise ApplicationException(
			errcode=ERROR_CONFIG_LOGIN_CODE_FIELD_NAME_WRONG,
		)
	return config_common.LOGIN_CODE_FIELD_NAME

def get_update_iv_field_name():
	if not isinstance(config_common.UPDATE_IV_FIELD_NAME, str):
		raise ApplicationException(
			errcode=ERROR_CONFIG_UPDATE_IV_FIELD_NAME_WRONG,
		)
	return config_common.UPDATE_IV_FIELD_NAME

def get_update_encryptedData_field_name():
	if not isinstance(config_common.UPDATE_ENCRYPTEDDATA_FIELD_NAME, str):
		raise ApplicationException(
			errcode=ERROR_CONFIG_UPDATE_ENCRYPTEDDATA_FIELD_NAME_WRONG,
		)
	return config_common.UPDATE_ENCRYPTEDDATA_FIELD_NAME

#----------------------------------
# auth weixin
#----------------------------------
#code2Session
def get_session_key_from_weixin(appid,appsecret,js_code):
	weixin_api = 'https://api.weixin.qq.com/sns/jscode2session'
	grant_type = 'authorization_code'
	url = '{}?appid={}&secret={}&js_code={}&grant_type={}'.format(
		weixin_api,
		appid,
		appsecret,
		js_code,
		grant_type,
	)
	return requests.get(url).json()

#----------------------------------
# auth decrypt token
#----------------------------------
def decrypt_token(token):
	cryption = Serializer(
		secret_key=get_token_secret_key(),
		salt=get_token_salt(),
		expires_in=get_token_timeout_hours() * 3600
	)

	try:
		result_token = cryption.loads(token)
		return result_token
	except SignatureExpired:
		raise ApplicationException(
			errcode=ERROR_TOKEN_TIMEOUT,
		)
	except:
		raise ApplicationException(
			errcode=ERROR_TOKEN_WRONG_DECRYPT,
		)


def encrypt_token(userinfo):
	cryption = Serializer(
		secret_key=get_token_secret_key(),
		salt=get_token_salt(),
		expires_in=get_token_timeout_hours() * 3600
	)
	try:
		result_token = cryption.dumps(userinfo)
		return result_token
	except:
		raise ApplicationException(
			errcode=ERROR_TOKEN_WRONG_ENCRYPT,
		)

#----------------------------------
# decrypt weixin
#----------------------------------
#decrypt
def decrypt(session_key, iv, encrypted):
	try:
		key = base64.b64decode(session_key)
		iv = base64.b64decode(iv)
		cipher = Cipher(
			algorithms.AES(key),
			modes.CBC(iv),
			backend=default_backend(),
		)
		decryptor = cipher.decryptor()
		plain = decryptor.update(base64.b64decode(encrypted)) + decryptor.finalize()
		unpadder = PKCS7(128).unpadder()
		decrypted = unpadder.update(plain)
		decrypted += unpadder.finalize()
		decrypted = json.loads(decrypted.decode('utf8'))
	except UtilsException:
		raise
	except:
		raise ApplicationException(
			errcode=ERROR_IV_ENCRYPTED_WRONG,
		)
	return decrypted


#----------------------------------
# mongoengine
# configure it please if you replace mongoengine with something else
#----------------------------------
def get_wechat_user_info_from_database(token):

	result_token = decrypt_token(token)

	for attribute in get_token_fields_required():
		if not result_token.get(attribute):
			raise ApplicationException(
				errcode=ERROR_TOKEN_WRONG_FIELDS,
			)
	try:
		user = User.objects.get(openid=result_token['openid'])
	except:
		raise ApplicationException(
			errcode=ERROR_TOKEN_WRONG_NO_USER,
		)
	if user:
		return user
	else:
		raise ApplicationException(
			errcode=ERROR_TOKEN_WRONG_NO_USER,
		)

