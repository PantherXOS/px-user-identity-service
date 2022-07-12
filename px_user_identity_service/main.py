'''PantherX User Identity Service'''

import logging
import platform

import falcon
import pkg_resources
from px_device_identity import is_superuser_or_quit
from requests.models import HTTPError
from waitress import serve

from .ciba import CIBAAuthentication
from .config import PORT
from .log import *
from .qr import QRAuthentication

log = logging.getLogger(__name__)


opsys = platform.system()
version = pkg_resources.require("px-user-identity-service")[0].version


class CORSComponent():
    def process_response(self, req: falcon.Request, resp: falcon.Response, resource, req_succeeded):
        '''Handles CORS'''
        resp.set_header('Access-Control-Allow-Origin', '127.0.0.1')

        if (req_succeeded
			and req.method == 'OPTIONS'
			and req.get_header('Access-Control-Request-Method')
		):

            allow = resp.get_header('Allow')
            resp.delete_header('Allow')

            allow_headers = req.get_header(
                'Access-Control-Request-Headers',
                default='127.0.0.1'
            )

            resp.set_headers((
                ('Access-Control-Allow-Methods', allow),
                ('Access-Control-Allow-Headers', allow_headers),
                ('Access-Control-Max-Age', '86400'),  # 24 hours
            ))


class UserQRAuthRequestRessource():
    def on_get(self, req: falcon.Request, resp: falcon.Response):
        """Received user QR authentication request"""

        try:
            resp.media = QRAuthentication().login()
            resp.status = falcon.code_to_http_status(202)
        except Exception as err:
            log.error(err)
            raise falcon.HTTPError(503, 'Service Unavailable', err)


class UserQRAuthStatusRessource():
    def on_get(self, req: falcon.Request, resp: falcon.Response, auth_req_id):
        """Received user QR authenication status request"""

        try:
            resp.media = QRAuthentication().status(auth_req_id)
            resp.status = falcon.code_to_http_status(202)
        except Exception as err:
            log.error(err)
            raise falcon.HTTPError(503, 'Service Unavailable', err)


class UserBCAuthRequestRessource():
    def on_post(self, req: falcon.Request, resp: falcon.Response):
        """Received user BC authentication request"""

        login_hint_token = req.media.get('login_hint_token', None)
        login_message = req.media.get('login_message', None)

        if login_hint_token is None:
            raise falcon.HTTPError(400, 'Bad request', 'Could not find required login_hint_token.')

        ciba = CIBAAuthentication()
        try:
            data = None
            if login_message is None:
                data = ciba.login(login_hint_token)
            else:
                data = ciba.login(login_hint_token, login_message)
            resp.status = falcon.code_to_http_status(202)
            resp.media = data
        except Exception as err:
            log.error(err)
            raise falcon.HTTPError(503, 'Service Unavailable', err)


class UserBCAuthStatusRessource():
    def on_get(self, req: falcon.Request, resp: falcon.Response, auth_req_id):
        """Received user BC authenication status request"""
        
        ciba = CIBAAuthentication()

        try:
            data = ciba.status(auth_req_id)

            resp.media = data
            resp.status = falcon.code_to_http_status(202)

        except HTTPError as err:
            if err.response.status_code == 400:
                resp.media = {
                    'message': err.response.json()['error_description'],
                    'status': 'pending'
                }
                resp.status = falcon.code_to_http_status(400)
        except Exception as err:
            log.error(err)
            raise falcon.HTTPError(503, 'Service Unavailable', err)


app = falcon.App(middleware=[CORSComponent()])

auth_ressource_qr_login = UserQRAuthRequestRessource()
auth_ressource_qr_status = UserQRAuthStatusRessource()
auth_ressource_bc_login = UserBCAuthRequestRessource()
auth_ressource_bc_status = UserBCAuthStatusRessource()

app.req_options.strip_url_path_trailing_slash = True

app.add_route('/auth/qr', auth_ressource_qr_login)
app.add_route('/auth/qr/{auth_req_id}', auth_ressource_qr_status)
app.add_route('/auth/bc', auth_ressource_bc_login)
app.add_route('/auth/bc/{auth_req_id}', auth_ressource_bc_status)


def main():
    '''Runs PantherX User Identity Service'''
    log.info('------')
    log.info(f"PantherX User Identity Service v{version}")
    log.info('------')

    is_superuser_or_quit()

    serve(app, listen=f"127.0.0.1:{PORT}")


if __name__ == '__main__':
    main()
