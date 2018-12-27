from gevent import monkey
monkey.patch_all()

from flask import Flask
from flask import request

from exception import IllegalRequestException

app = Flask(__name__)


class Response(object):
    pass


class FooException(Exception):
    pass


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def echo(path):
    method = request.method
    headers = request.headers

    return 'path: {path}\n' \
           'method: {method}\n' \
           'headers: {headers}\n' \
           'data: {data}'.strip().format(path=path, method=method, headers=headers, data=request.data)


@app.route('/status/<code>')
def status(code):
    try:
        status_code = int(code)

        return 'as you wish...', status_code
    except ValueError:
        return 'illegal status code: %s' % code


@app.route('/raise_exception')
def runtime_exception():
    raise RuntimeError('raise runtim exception on purpose')


@app.route('/foo_exception')
def foo_exception():
    raise FooException('raise foo exception on purpose')


@app.route('/bar_exception/<service_path>')
def bar_exception(service_path):
    raise IllegalRequestException(u'unknown service: ' + service_path)


@app.route('/sys-status/')
def sys_status():
    return 'echo v1.1'


if __name__ == '__main__':
    app.run()
