'''PantherX User Identity Service'''

import logging
import platform

import pkg_resources
from flask import Flask, request, jsonify, make_response
from px_device_identity import is_superuser_or_quit
from requests.models import HTTPError
from werkzeug.middleware.proxy_fix import ProxyFix
from waitress import serve

from .common import CommonAuthentication
from .ciba import CIBAAuthentication
from .config import PORT
from .log import *
from .qr import QRAuthentication

log = logging.getLogger(__name__)

opsys = platform.system()
version = pkg_resources.require("px-user-identity-service")[0].version

app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app)

@app.after_request
def cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '127.0.0.1'
    if request.method == 'OPTIONS':
        response.headers['Access-Control-Allow-Methods'] = response.headers.get('Allow', '127.0.0.1')
        response.headers['Access-Control-Allow-Headers'] = request.headers.get('Access-Control-Request-Headers', '127.0.0.1')
        response.headers['Access-Control-Max-Age'] = '86400'  # 24 hours
    return response

@app.route('/auth/qr', methods=['GET', 'OPTIONS'])
def qr_auth_request():
    if request.method == 'OPTIONS':
        return make_response('', 204)

    try:
        data = QRAuthentication().login()
        return make_response(jsonify(data), 202)
    except Exception as err:
        log.error(err)
        return make_response(jsonify(title='Client error', description=str(err)), 400)

@app.route('/auth/qr/<auth_req_id>', methods=['GET', 'OPTIONS'])
def qr_auth_status(auth_req_id):
    if request.method == 'OPTIONS':
        return make_response('', 204)

    try:
        data = QRAuthentication().status(auth_req_id)
        return make_response(jsonify(data), 202)
    except Exception as err:
        log.error(err)
        return make_response(jsonify(title='Client error', description=str(err)), 400)

@app.route('/auth/refresh', methods=['POST', 'OPTIONS'])
def common_auth_refresh():
    if request.method == 'OPTIONS':
        return make_response('', 204)

    access_token = request.json.get('access_token', None)
    refresh_token = request.json.get('refresh_token', None)
    grant_type = 'refresh_token'

    if access_token is None or refresh_token is None:
        return make_response(jsonify(title='Bad request', description='The access_token and refresh_token are required.'), 400)

    auth = CommonAuthentication()
    try:
        data = auth.refresh(refresh_token, grant_type)
        return make_response(jsonify(data), 200)
    except Exception as err:
        log.error(err)
        return make_response(jsonify(title='Client error', description='Could not refresh token.'), 400)

@app.route('/auth/bc', methods=['POST', 'OPTIONS'])
def bc_auth_request():
    if request.method == 'OPTIONS':
        return make_response('', 204)

    login_hint_token = request.json.get('login_hint_token', None)
    login_message = request.json.get('login_message', None)

    if login_hint_token is None:
        return make_response(jsonify(title='Bad request', description='The login_hint_token is required.'), 400)

    ciba = CIBAAuthentication()
    try:
        data = None
        if login_message is None:
            data = ciba.login(login_hint_token)
        else:
                        data = ciba.login(login_hint_token, login_message)
        return make_response(jsonify(data), 202)
    except Exception as err:
        log.error(err)
        return make_response(jsonify(title='Client error', description=str(err)), 400)

@app.route('/auth/bc/<auth_req_id>', methods=['GET', 'OPTIONS'])
def bc_auth_status(auth_req_id):
    if request.method == 'OPTIONS':
        return make_response('', 204)

    ciba = CIBAAuthentication()

    try:
        data = ciba.status(auth_req_id)
        return make_response(jsonify(data), 202)
    except HTTPError as err:
        if err.response.status_code == 400:
            return make_response(jsonify(message=err.response.json()['error_description'], status='pending'), 400)
    except Exception as err:
        log.error(err)
        return make_response(jsonify(title='Client error', description=str(err)), 400)

def main():
    '''Runs PantherX User Identity Service'''
    log.info('------')
    log.info(f"PantherX User Identity Service v{version}")
    log.info('------')

    is_superuser_or_quit()

    serve(app, host='127.0.0.1', port=PORT)

if __name__ == '__main__':
    main()

