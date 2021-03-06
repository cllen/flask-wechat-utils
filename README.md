
flask-wechat-utils
===================
* v0.1.16
* mongo/python2.7
* 封装了微信用户登录，注册，验证，消息模板等4个功能:
- [x] 微信用户登录(code)
- [x] 微信用户注册(iv,encryptedData,...)
- [x] 微信用户验证(token)
- [x] 存储formid,过期自动删除
- [x] 发送模板消息给用户
* django框架下也有同样功能的第三方库: django-wechat-utils




quickstart
===================
* 五步骤完成快速开始

1 安装：mongo,如果已经安装,跳过。
-------------------
```bash
apt-get install mongodb
```

2 安装：flask-wechat-utils。
-------------------
```bash
pip install flask-wechat-utils
```

3 编写：run.py ，配置mongodb、appid、appsecret。
-------------------
```python
#coding:utf8
from flask import Flask
import flask_wechat_utils

app = Flask(__name__)

#-------------------------------------------
# 1 config
#-------------------------------------------
app.config['MONGODB_SETTINGS'] = {
	'db': 'xxx',
	'host': '127.0.0.1',
	'port': 27017,
}

app.config['WXAPP_ID'] 		= 'xxx' #小程序appid
app.config['WXAPP_SECRET'] 	= 'xxx' #小程序secret
app.config['WEB_NAME'] 		= 'myweb' #路由的
app.config['TEMPLATE_ID']	= None #小程序消息模板ID

#-------------------------------------------
# 2 init (db/bp/api)
#-------------------------------------------
flask_wechat_utils.init_app(app)

#-------------------------------------------
# 3 routes
#-------------------------------------------
from flask_wechat_utils.user import routes				#使用默认user路由
from flask_wechat_utils.message_template import routes	#使用默认message_template路由

if __name__ == '__main__':
	app.run(host='0.0.0.0',port=5000)
```

4 运行：run.py。
-------------------
```bash
python run.py
```
* 查看接口文档：http://127.0.0.1:5000/myweb

5 使用：微信小程序分别带上code、iv、encryptedData、token访问下面api完成用户信息的登录、验证、注册。这里提供的是python模拟微信小程序访问。
-------------------
* login
```python
import requests
url = 'http:127.0.0.1:5000/myweb/user'
headers = {
	'Content-Type':'application/json',
}
data = {
	'code':'xxx',
}
response = requests.post(url,headers=headers,json=data)
print response.json() #token
```

* auth
```python
import requests
url = 'http:127.0.0.1:5000/myweb/user'
headers = {
	'Content-Type':'application/json',
	'token':'xxx',
}
response = requests.get(url,headers=headers)
print response.json()
```

* register
```python
import requests
url = 'http:127.0.0.1:5000/myweb/user'
headers = {
	'Content-Type':'application/json',
	'token':'xxx',
}
data = {

	#使用这些字段
	'nickname':'xxx',
	'avatar':'xxx',
	'gender':'xxx',
	'city':'xxx',
	'province':'xxx',
	'country':'xxx',
	'language':'xxx',

	#或使用这两个字段
	'encryptedData':'xxx',
	'iv':'xxx',
}
response = requests.put(url,headers=headers,json=data)
print response.json()
```

done
-------------------
* 完成，以上是快速开始的3个接口示例。
* auth,login,register,消息模板的具体使用请参考github的examples/big示例。
* 作者邮箱:13250270761@163.com
* 项目地址:https://github.com/suckmybigdick/flask-wechat-utils
* 有任何疑问或任何bug请发送到我邮箱，我会在第一时间回复并修复，同时感谢您提交的任何问题。

ps:目录结构
-------------------

web  
├── __init__.py  
├── config.py  
├── run.py  
├── application1  
├── application2  
└── application3  
     ├── config.py  
     ├── exceptions.py  
     ├── __init__.py  
     ├── models.py  
     ├── routes.py  
     └── utils.py  