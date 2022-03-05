'''CIBA Authentication'''
import logging

from px_device_identity import Device, DeviceProperties
from px_device_identity.device.jwt import (
    generate_signature_content_from_dict, get_unix_time_in_seconds
)
from px_device_identity.device.sign import Sign
from requests import ConnectionError, post

log = logging.getLogger(__name__)


class CIBAAuthentication():
    '''CIBA Authentication'''

    def __init__(self):
        device = Device()
        self.device_properties: 'DeviceProperties' = device.properties
        self.device_jwt = device.get_device_jwt()['device_jwt']

    def _auth_request(self, login_hint_token: str, message: str):
        iat = get_unix_time_in_seconds()
        exp = iat + 300
        initial_request = {
            'login_hint_token': login_hint_token,
            'scope': 'openid contact profile',
            'acr_values': 'poll',
            'iss': self.device_properties.client_id,
            'aud': "{}/oidc/bc-authorize".format(self.device_properties.host),
            'exp': exp,
            'binding_message': message
        }
        signature_content = generate_signature_content_from_dict(
            initial_request, iat, exp)
        signature = Sign(self.device_properties, signature_content).sign()
        result = "{}.{}".format(signature_content, signature)
        return result

    def _auth_request_content(self, login_hint_token: str, message: str):
        '''CIBA auth request content'''
        auth_request = {
            "request": self._auth_request(login_hint_token, message),
            "client_id": self.device_properties.client_id,
            "client_assertion_type": "urn:ietf:params:oauth:client-assertion-type:jwt-bearer",
            "client_assertion": self.device_jwt,
        }
        return auth_request

    def _status_request_content(self, auth_req_id: str):
        '''CIBA status request content'''
        status_request = {
            'grant_type': 'urn:openid:params:grant-type:ciba',
            'auth_req_id': auth_req_id,
            'client_id': self.device_properties.client_id,
            'client_assertion_type': 'urn:ietf:params:oauth:client-assertion-type:jwt-bearer',
            'client_assertion': self.device_jwt
        }
        return status_request

    def _make_request(self, url: str, data: dict):
        '''Make API request'''
        try:
            res = post(url, data=data, headers={
                'Accept': 'application/json, text/plain, */*',
                'Content-Type': 'application/x-www-form-urlencoded'
            })
            res.raise_for_status()
            return res.json()
        except ConnectionError as err:
            log.error("Connection to {} failed.".format(url))
            raise err
        except Exception as err:
            log.error(err)
            raise err

    def login(self, login_hint_token: str, message: str = 'Authorize Login'):
        '''
        CIBA (Backchannel) login request

        Params:
            login_hint_token: username
            message: Optional login message
                     Recommended format 'Authorize login to ApplicationName'
        '''
        log.debug('=> CIBA login request for {}'.format(login_hint_token))
        url = self.device_properties.host + '/oidc/bc-authorize'
        return self._make_request(url, self._auth_request_content(login_hint_token, message))

    def status(self, auth_req_id: str):
        '''CIBA (Backchannel) login status request'''
        log.debug('=> CIBA login status request for ID {}'.format(auth_req_id))
        url = self.device_properties.host + '/oidc/token'
        return self._make_request(url, self._status_request_content(auth_req_id))
