'''QR Authentication'''
import logging

from px_device_identity import DeviceProperties, Device
from requests import ConnectionError, get

log = logging.getLogger(__name__)


class QRAuthentication:
    '''QR Authentication'''

    def __init__(self):
        device = Device()
        self.device_properties: DeviceProperties = device.properties
        self.access_token: str = device.get_access_token()['access_token']

    def _make_request(self, url: str, access_token: str):
        '''Initiate API request'''
        log.debug('=> Making request to {}'.format(url))
        try:
            res = get(url, headers={
                'authorization': 'Bearer {}'.format(access_token)
            })
            return res.json()
        except ConnectionError as err:
            log.error("Connection to {} failed.".format(url))
            raise err
        except Exception as err:
            log.error(err)
            raise err

    def login(self):
        '''Request user QR authentication grant'''
        log.debug('=> Getting user auth grant')
        url = f"{self.device_properties.host}/auth/qr"
        data = self._make_request(url, self.access_token)
        # auth_req_id, exp
        return data

    def status(self, auth_req_id: str):
        '''Request user QR authentication grant status'''
        log.debug('=> Getting user auth request status')
        url = f"{self.device_properties.host}/auth/qr/{auth_req_id}"
        data = self._make_request(url, self.access_token)
        # status, access_token, issue_time
        return data
