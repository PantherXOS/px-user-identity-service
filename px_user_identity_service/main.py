'''PantherX User Identity Service'''

import logging
import platform
import sys

import falcon
import pkg_resources
from px_device_identity import Device, is_superuser_or_quit
from waitress import serve

from .cm import CM
from .config import PORT
from .log import *

log = logging.getLogger(__name__)


opsys = platform.system()
version = pkg_resources.require("px-user-identity-service")[0].version


class CORSComponent():
    def process_response(self, req, resp, resource, req_succeeded):
        '''Handles CORS'''
        # TODO: Consider changing to: 127.0.0.1
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

class UserAuthRequestRessource():
    def on_get(self, req, resp):
        """Received user authentication request"""
        device = Device()
        device_properties: 'DeviceProperties' = device.properties
        access_token = device.get_access_token()
        print(access_token['access_token'])
        cm = CM(device_properties)
        try:
            data = cm.get_user_qr_auth_grant(access_token['access_token'])

            resp.status = falcon.HTTP_202
            resp.media = data
        except Exception as err:
            log.error(err)
            resp.status = falcon.HTTP_503


class UserAuthStatusRessource():
    def on_get(self, req, resp, auth_req_id):
        """Received user authenication status request"""

        device = Device()
        device_properties: 'DeviceProperties' = device.properties
        access_token = device.get_access_token()
        cm = CM(device_properties, auth_req_id)
        try:
            data = cm.get_user_qr_auth_status(access_token['access_token'])

            resp.status = falcon.HTTP_202
            if access_token:
                resp.media = data
            else:
                resp.media = {
                    "status": status
                }
        except Exception as err:
            log.error(err)
            resp.status = falcon.HTTP_503


app = falcon.API(middleware=[CORSComponent()])
auth_request_grant = UserAuthRequestRessource()
auth_request_status = UserAuthStatusRessource()

app.req_options.strip_url_path_trailing_slash = True
app.add_route('/auth/qr', auth_request_grant)
app.add_route('/auth/qr/{auth_req_id}', auth_request_status)


def main():
    '''Runs PantherX User Identity Service'''
    log.info('------')
    log.info('Welcome to PantherX User Identity Service')
    log.info('v{}'.format(version))
    log.info('------')

    is_superuser_or_quit()

    serve(app, listen='127.0.0.1:{}'.format(PORT))

if __name__ == '__main__':
    main()
