
flask-wechat-utils
===================
* v0.1.7
* 最后修改时间：2019年01月14日15:28:53
* 最后修改时间：2019年01月30日14:43:54
* 基于:python2,flask,mongo,
* Restful的微服务代码风格
* 封装了微信用户登录，注册，验证，消息模板等4个功能:
- [x] 微信用户登录(openid)
- [x] 微信用户注册(nickname,avatarUrl,...)
- [x] 微信用户验证(token)
- [x] 新增：formid存储/读出自动删除/过期自动删除
- [x] 新增：微信消息模板发送




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

#-------------------------------------------
# app
#-------------------------------------------
app = Flask(__name__)

#-------------------------------------------
# config
#-------------------------------------------
app.config['MONGODB_SETTINGS'] = {
	'db': 'blog',
	'host': 'mongo',
	'port': 27017,
}

app.WXAPP_ID = 'xxx'
app.WXAPP_SECRET = 'xxx'
app.TOKEN_SECRET_KEY = 'xxx'
app.TOKEN_SALT = 'xxx'
app.TOKEN_TIMEOUT_HOURS = 24 * 365
app.WEB_NAME = 'myweb'
app.TEMPLATE_ID = None

#-------------------------------------------
# config flask-wechat-utils (db/bp/api)
#-------------------------------------------
flask_wechat_utils.init_app(app)

#-------------------------------------------
# register bp
#-------------------------------------------
app.register_blueprint(flask_wechat_utils.config.bp)

#-------------------------------------------
# route
#-------------------------------------------
from flask_wechat_utils.user import routes
from flask_wechat_utils.message_template import routes


if __name__ == '__main__':
	app.run(host='0.0.0.0',port=5000)

```

4 运行：run.py。
-------------------
```bash
python run.py
```

5 测试：微信小程序分别带上code、iv、encryptedData、token访问下面api完成用户信息的登录、验证、注册。这里提供的是python模拟微信小程序访问。
-------------------
* login
```python
import requests
url = 'http:127.0.0.1:5000/myweb/wechat/user'
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
url = 'http:127.0.0.1:5000/myweb/wechat/test'
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
url = 'http:127.0.0.1:5000/myweb/wechat/user'
headers = {
	'Content-Type':'application/json',
	'token':'xxx',
}
data = {
	'nickname':'xxx',
	'avatar':'xxx',
	'gender':'xxx',
	'city':'xxx',
	'province':'xxx',
	'country':'xxx',
	'language':'xxx',
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
* 该项目的目录结构:  
flask_wechat_utils  
├── __init__.py  
├── config.py  
├── user  
│   ├── config.py  
│   ├── exceptions.py  
│   ├── __init__.py  
│   ├── models.py  
│   ├── routes.py  
│   └── utils.py  
└── message_template  
     ├── config.py  
     ├── exceptions.py  
     ├── __init__.py  
     ├── models.py  
     ├── routes.py  
     └── utils.py  
* 用户可以参考该目录结构：  
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