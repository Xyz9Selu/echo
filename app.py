import sys

from gevent import monkey
monkey.patch_all()

from flask import Flask
from flask import request

app = Flask(__name__)
if 'DEBUG' in sys.argv:
    app.config['DEBUG'] = sys.argv['DEBUG']


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
    debug = request.args.get('debug', None)
    if debug is not None:
        app.config['DEBUG'] = debug

    raise RuntimeError('raise runtim exception on purpose')


@app.route('/sys-status/')
def sys_status():
    return 'echo v1.1'


if __name__ == '__main__':
    app.run()
