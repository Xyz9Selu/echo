FROM python:3.11-slim AS base

# 设置环境变量
ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONFAULTHANDLER 1

# 缓存层
FROM base AS python-deps

# 安装Pipenv及其它编译依赖
RUN pip install pipenv -i https://pypi.douban.com/simple/
RUN sed -i 's,[a-z\.]*\.debian.org,mirrors.aliyun.com,g' /etc/apt/sources.list
RUN apt-get update
RUN apt-get install -y --no-install-recommends build-essential

# 安装Python依赖于/.venv
COPY Pipfile .
COPY Pipfile.lock .
RUN PIPENV_VENV_IN_PROJECT=1 pipenv install --deploy
RUN PIPENV_VENV_IN_PROJECT=1 pipenv install --deploy --skip-lock uwsgi


# 服务层
FROM base AS runtime

# 将安装好的依赖拷贝至当前层
# pip install -i https://pypi.douban.com/simple/ --no-cache-dir uwsgi
COPY --from=python-deps /.venv /.venv
ENV PATH="/.venv/bin:$PATH"

WORKDIR /src

# Install application into container
COPY . .

# Run the application
CMD uwsgi --processes=1 -M --gevent=100 --http :80 -w app:app
