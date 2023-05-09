from gevent import monkey
monkey.patch_all()

import os

from flask import Flask
from flask import request
from flask import make_response
from pprint import pformat
import requests

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


@app.route('/raise-exception')
def runtime_exception():
    debug = request.args.get('debug', None)
    if debug is not None:
        app.config['DEBUG'] = debug

    raise RuntimeError('raise runtim exception on purpose')


@app.route('/access-url')
def access_url():
    url = request.args.get('url', None)
    if url is None:
        return 'url is required', 400

    method = request.args.get('method', 'GET')
    headers = request.args.get('headers', None)
    data = request.args.get('data', None)

    try:
        response = requests.request(method, url, headers=headers, data=data)

        flask_response = make_response(response.content, response.status_code)

        for k, v in response.headers.items():
            if k.lower() not in ('content-encoding', 'transfer-encoding'):
                flask_response.headers[k] = v

        return flask_response
    except Exception as e:
        return 'error: %s' % e, 500


@app.route('/sys-status/')
def sys_status():
    return 'echo v1.2'


if __name__ == '__main__':
    app.run(debug=True, port=5001)
