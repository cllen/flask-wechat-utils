
flask-wechat-utils v0.1.1
===================
* 最后修改时间：2019年01月11日18:54:45
* 基于:mongo,flask
* 微服务 + Restful 的代码风格
* 封装了微信用户登录，注册，验证，消息模板等4个功能:
- [x] 微信用户登录(openid)
- [x] 微信用户注册(nickname,avatarUrl,...)
- [x] 微信用户验证(token)
- [x] 新增：formid写入+读出后自动删除+过期后自动删除
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

from flask_wechat_utils import bp as wechat_bp
from flask_wechat_utils import db as wechat_db
from flask_wechat_utils import config as wechat_config

#-------------------------------------------
# app
#-------------------------------------------
app = Flask(__name__)

#-------------------------------------------
# config
#-------------------------------------------
app.config['MONGODB_SETTINGS'] = {
	'db': 'xxx',
	'host': 'mongo',
	'port': 27017,
}

wechat_config.WXAPP_ID = 'xxx'
wechat_config.WXAPP_SECRET = 'xxx'
wechat_config.WEB_NAME = 'myweb'

#-------------------------------------------
# 固定写法，不需要修改，初始化数据库+注册路由
#-------------------------------------------
wechat_db.init_app(app)
app.register_blueprint(wechat_bp)

#-------------------------------------------
# 用户写好自己的application的route,model等,然后这里导入路由即可,这里使用该库默认路由
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
* 完成，以上是快速开始的3个接口，还有消息模板接口请参考github的examples/big示例。
* 作者邮箱:13250270761@163.com
* 项目地址:https://github.com/suckmybigdick/flask-wechat-utils
* 有任何疑问或任何bug请发送到我邮箱，我会在第一时间回复并修复，同时感谢您提交的任何问题。
