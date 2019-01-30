#coding:utf8
from flask_wechat_utils.utils import now_ts
from flask_wechat_utils.config import db 
from config import EXPIRE_AFTER_SECONDS

from datetime import datetime

class MessageTemplate(db.Document):

	openid = db.StringField(fefault=None)
	form_id = db.StringField(default=None)
	created_ts = db.DateTimeField(default=datetime.utcnow)

	meta = {
		'collection': 'message_template',
		'indexes': [
			{
				'fields': ['created_ts'],
				'expireAfterSeconds':EXPIRE_AFTER_SECONDS,
			},
		],
	}