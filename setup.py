import setuptools


# with open("README.md", "r") as fh:
# 	long_description = fh.read()

long_description = 'https://github.com/suckmybigdick/flask-wechat-utils'


setuptools.setup(
	name = "flask-wechat-utils",
	version="0.1.16",
	auth="Huang Xu Hui",
	author_email="13250270761@163.com",
	description="flask-wechat-tuils for wechat-app-user's login/register/auth, and message_template",
	long_description=long_description,
	long_description_content_type="text/markdown",
	url="https://github.com/suckmybigdick/flask-wechat-utils",
	packages=setuptools.find_packages(),
	classifiers=[
		"Programming Language :: Python :: 2",
		"License :: OSI Approved :: MIT License",
		"Operating System :: OS Independent",
	],
	install_requires=[
		"Flask==0.10.1",
		"requests==2.9.1",
		"cryptography",
		"itsdangerous==0.24",
		"Werkzeug==0.15.3",
		"flask_restplus==0.12.1",
		"flask_mongoengine==0.9.5",
	],
)




