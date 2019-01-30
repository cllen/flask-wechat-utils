FROM python:2.7

RUN mkdir -p /home/hxh/myweb
WORKDIR /home/hxh/myweb
RUN apt-get update
#RUN apt-get install apt-uitls -y
RUN apt-get install build-essential libssl-dev libffi-dev python-dev -y
RUN pip install --upgrade pip
RUN pip install cryptography
COPY requirements.txt /home/hxh/myweb
RUN pip install --no-cache-dir -r requirements.txt

COPY . /home/hxh/myweb

