#coding:utf8
from flask_wechat_utils.config import db
from flask_wechat_utils.utils import now_ts

#model
class Blog(db.Document):
	openid = db.StringField(default=None)
	text = db.StringField()
	created_ts = db.IntField(default=now_ts)

	meta = {
		'collection': 'blog',
		'indexes': [
			{
				'fields': ['openid'],
			},
		],
		'strict': False,
	}
