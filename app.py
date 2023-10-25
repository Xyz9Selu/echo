from gevent import monkey

monkey.patch_all()

import os

from flask import Flask
from flask import request
from flask import make_response
from flask import send_from_directory
from pprint import pprint
from pprint import pformat
import requests
from datetime import datetime


app = Flask(__name__)
if "DEBUG" in os.environ:
    print("found DEBUG=%s in environment" % os.environ["DEBUG"])
    app.config["DEBUG"] = os.environ["DEBUG"] in ("true", "True", "TRUE")
    print("set app config: DEBUG=%s" % app.config["DEBUG"])


@app.route(
    "/",
    defaults={"path": ""},
    methods=[
        "GET",
        "HEAD",
        "POST",
        "PUT",
        "DELETE",
        "CONNECT",
        "OPTIONS",
        "TRACE",
        "PATCH",
    ],
)
@app.route(
    "/<path:path>",
    methods=[
        "GET",
        "HEAD",
        "POST",
        "PUT",
        "DELETE",
        "CONNECT",
        "OPTIONS",
        "TRACE",
        "PATCH",
    ],
)
def echo(path):
    method = request.method
    headers = request.headers
    scheme = request.scheme

    data = request.get_data()
    args = pformat(request.args.to_dict())
    form = pformat(request.form.to_dict())

    result = (
        "scheme: {scheme}\n"
        "path: {path}\n"
        "method: {method}\n"
        "headers: \n{headers}\n"
        "data: {data}\n"
        "-----------------------------------------end data-----------------------------------------\n"
        "args: {args}\n"
        "form: {form}".strip().format(
            scheme=scheme,
            path=path,
            method=method,
            headers=headers,
            data=data,
            args=args,
            form=form,
        )
    )

    pprint(result)
    return result


@app.route("/status/<code>")
@app.route("/status/<code>/")
def status(code):
    try:
        status_code = int(code)

        result = "as you wish...", status_code
    except ValueError:
        result = "illegal status code: %s" % code

    pprint(result)
    return result


@app.route("/raise-exception")
@app.route("/raise-exception/")
def runtime_exception():
    debug = request.args.get("debug", None)
    if debug is not None:
        app.config["DEBUG"] = debug

    msg = "raise runtim exception on purpose"
    pprint(f"exception: {msg}")
    raise RuntimeError(msg)


@app.route("/ip")
@app.route("/ip/")
@app.route("/ipinfo")
@app.route("/ipinfo/")
def ipinfo():
    # Get the client's IP address
    client_ip = request.remote_addr

    # Return the client's IP address as the response
    pprint(f"ip: {client_ip}")
    return client_ip


@app.route("/time")
@app.route("/time/")
def get_time():
    now = datetime.now()
    return now.strftime("%Y-%m-%d %H:%M:%S")


@app.route("/access-url")
@app.route("/access-url/")
def access_url():
    url = request.args.get("url", None)
    if url is None:
        return "url is required", 400

    method = request.args.get("method", "GET")
    headers = request.args.get("headers", None)
    data = request.args.get("data", None)

    try:
        response = requests.request(method, url, headers=headers, data=data)

        # Check if the response body is larger than 10k
        if len(response.content) > 32 * 1024:
            return "Content Too Large", 413

        flask_response = make_response(response.content, response.status_code)

        for k, v in response.headers.items():
            if k.lower() not in ("content-encoding", "transfer-encoding"):
                flask_response.headers[k] = v

        pprint(f"access url: {url}")
        return flask_response
    except Exception as e:
        return "error: %s" % e, 500


@app.route("/sys-status")
@app.route("/sys-status/")
def sys_status():
    result = "echo v1.3"
    return result


@app.route("/favicon.ico")
def favicon():
    return send_from_directory(
        os.path.join(app.root_path, "static"),
        "favicon.ico",
        mimetype="image/vnd.microsoft.icon",
    )


if __name__ == "__main__":
    app.run(debug=True, port=5001)
