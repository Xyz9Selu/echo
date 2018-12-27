FROM python:2.7

# set timezone
ENV TZ=Asia/Shanghai
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# install software
RUN pip install uwsgi

# install python requirements.txt
ADD ./requirements.txt requirements.txt
RUN pip install -r requirements.txt

# copy config files
COPY . /src

# create logs dir
RUN mkdir /var/log/echo/

WORKDIR /src

EXPOSE 80
CMD uwsgi --processes=1 -M --gevent=100 --http-socket :80 -w echo:app
