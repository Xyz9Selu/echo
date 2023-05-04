FROM python:3.11-slim

# set time zone
ENV TZ=Asia/Shanghai
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# copy requirements
ADD $PROJ_FOLDER/requirements.txt requirements.txt

# 安装依赖
RUN apt-get update && apt-get install -y --no-install-recommends build-essential default-libmysqlclient-dev && \
pip install --no-cache-dir -r requirements.txt && \
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
