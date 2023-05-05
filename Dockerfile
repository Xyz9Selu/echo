FROM python:3.11-slim

# set time zone
ENV TZ=Asia/Shanghai
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# copy requirements
ADD ./requirements.txt requirements.txt

# 安装依赖
RUN sed -i 's,[a-z\.]*\.debian.org,mirrors.aliyun.com,g' /etc/apt/sources.list && \
apt-get update && apt-get install -y --no-install-recommends build-essential default-libmysqlclient-dev && \
pip install -i https://pypi.douban.com/simple/ --no-cache-dir -r requirements.txt && \
pip install -i https://pypi.douban.com/simple/ --no-cache-dir uwsgi && \
apt-get purge -y build-essential && \
apt-get autoremove -y && apt-get autoclean

RUN pip install uwsgi

# 拷贝项目文件
COPY . /src

# 其它工作...
RUN mkdir /var/log/echo/

WORKDIR /src

EXPOSE 80

CMD uwsgi --processes=1 -M --gevent=100 --http :80 -w app:app
