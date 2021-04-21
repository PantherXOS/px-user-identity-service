import json
import logging

from requests import ConnectionError, get, post

log = logging.getLogger(__name__)


class CM:
    '''Central Management communication'''
    def __init__(self, device_properties: 'DeviceProperties', auth_req_id: str = None):
        self.device_properties = device_properties
        self.auth_req_id = auth_req_id

        self.user_auth_grant_url = self.device_properties.host + '/auth/qr'
        self.user_auth_status_url = None
        if self.auth_req_id is not None:
            self.user_auth_status_url = self.device_properties.host + '/auth/qr/{}'.format(auth_req_id)

    def _make_request(self, url: str, access_token: str):
        '''Initiate API request'''
        log.debug('=> Making request to {}'.format(url))
        headers = {
            'authorization': 'Bearer {}'.format(access_token)
        }
        res = get(url, headers=headers)
        return res.json()

    def get_user_qr_auth_grant(self, access_token: str):
        '''Request user QR authentication grant'''
        log.debug('=> Getting user auth grant')
        data = self._make_request(self.user_auth_grant_url, access_token)
        # auth_req_id, exp
        return data
    
    def get_user_qr_auth_status(self, access_token: str):
        '''Request user QR authentication grant status'''
        log.debug('=> Getting user auth request status')
        if self.user_auth_grant_url is None:
            raise Exception('No authentication request ID has been provided')
        data = self._make_request(self.user_auth_status_url, access_token)
        # status, access_token, issue_time
        return data
