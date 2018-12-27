from flask import Flask
from flask import request

app = Flask(__name__)


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
def not_found(code):
    try:
        status_code = int(code)

        return 'as you wish...', status_code
    except ValueError:
        return 'illegal status code: %s' % code


@app.route('/sys-status/')
def sys_status():
    return 'echo v1.1'


if __name__ == '__main__':
    app.run()
