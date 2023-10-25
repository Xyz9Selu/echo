FROM python:3.11-slim-buster AS base

# 设置环境变量
ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONFAULTHANDLER 1

# 缓存层
FROM base AS python-deps

# 安装Pipenv及其它编译依赖
RUN pip install pipenv -i https://mirrors.aliyun.com/pypi/simple
RUN sed -i 's,[a-z\.]*\.debian.org,mirrors.aliyun.com,g' /etc/apt/sources.list
RUN apt-get update
RUN apt-get install -y build-essential default-libmysqlclient-dev

# 安装Python依赖于/.venv
COPY Pipfile .
COPY Pipfile.lock .
RUN PIPENV_VENV_IN_PROJECT=1 pipenv install --deploy --skip-lock
RUN PIPENV_VENV_IN_PROJECT=1 pipenv install --deploy --skip-lock uwsgi

# 服务层
FROM base AS runtime

# 将安装好的依赖拷贝至当前层
# pip install -i https://mirrors.aliyun.com/pypi/simple --no-cache-dir uwsgi
COPY --from=python-deps /.venv /.venv
ENV PATH="/.venv/bin:$PATH"
ENV GEVENT_SUPPORT=True

RUN sed -i 's,[a-z\.]*\.debian.org,mirrors.aliyun.com,g' /etc/apt/sources.list && \
    apt-get update && \
    apt-get install -y telnet curl inetutils-ping vim && \
    apt-get autoremove -y && apt-get clean && rm -rf /var/lib/apt/lists/*


WORKDIR /src

# Install application into container
COPY . .

ENV TZ=Asia/Shanghai

# Run the application
CMD uwsgi --processes=1 -M --gevent=100 --http :80 -w app:app
