# from gevent import monkey
# monkey.patch_all()

import os

from flask import Flask
from flask import request
from pprint import pformat

app = Flask(__name__)
if 'DEBUG' in os.environ:
    print('found DEBUG=%s in environment' % os.environ['DEBUG'])
    app.config['DEBUG'] = os.environ['DEBUG'] in ('true', 'True', 'TRUE')
    print('set app config: DEBUG=%s' % app.config['DEBUG'])


@app.route('/', defaults={'path': ''}, methods=['GET', 'HEAD', 'POST', 'PUT', 'DELETE', 'CONNECT', 'OPTIONS', 'TRACE', 'PATCH'])
@app.route('/<path:path>', methods=['GET', 'HEAD', 'POST', 'PUT', 'DELETE', 'CONNECT', 'OPTIONS', 'TRACE', 'PATCH'])
def echo(path):
    method = request.method
    headers = request.headers

    data = request.get_data()
    args = pformat(request.args.to_dict())
    form = pformat(request.form.to_dict())

    return 'path: {path}\n' \
           'method: {method}\n' \
           'headers: {headers}\n' \
           'data: {data}\n' \
           '-----------------------------------------end data-----------------------------------------\n' \
           'args: {args}\n' \
           'form: {form}'\
        .strip().format(path=path, method=method, headers=headers, data=data, args=args, form=form)


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
    app.run(debug=True)
