#coding:utf8
from flask_mongoengine import MongoEngine
from flask import current_app
from utils import now_ts

#db = MongoEngine()
from flask_wechat_utils.models import db

#model
class Blog(db.Document):
	openid = db.StringField(fefault=None)
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