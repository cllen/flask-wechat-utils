FROM python:2.7

RUN mkdir -p /home/hxh/myweb
WORKDIR /home/hxh/myweb
COPY requirements.txt /home/hxh/myweb
RUN pip install --no-cache-dir -r requirements.txt

COPY . /home/hxh/myweb