#coding:utf8
from flask_wechat_utils.utils import now_ts
from flask_wechat_utils.config import db 

class User(db.Document):

	openid = db.StringField(default=None)
	unionid = db.StringField()
	wxid = db.StringField()
	nickname = db.StringField()
	avatar = db.StringField()
	gender = db.IntField()
	city = db.StringField()
	province = db.StringField()
	country = db.StringField()
	language = db.StringField()

	session_key = db.StringField()
	mobile = db.StringField()
	last_login_ts = db.IntField(default=now_ts)
	last_ping_ts = db.IntField(default=now_ts)

	status = db.IntField(default=1)
	created_ts = db.IntField(default=now_ts)

	meta = {
		'collection': 'wechat_user',
		'indexes': [
			{
				'fields': ['openid'],
			},
			{
				'fields': ['unionid'],
			},
		],
	}


