'''Common Authentication'''
import logging

from px_device_identity import Device, DeviceProperties
from requests import ConnectionError, post

log = logging.getLogger(__name__)


class CommonAuthentication:
    '''Common Authentication'''

    def __init__(self):
        device = Device()
        self.device_properties: DeviceProperties = device.properties
        self.get_device_jwt = device.get_device_jwt


    def refresh(self, refresh_token: str, grant_type: str = 'refresh_token'):
        '''Refresh token'''
        log.debug('=> Requesting new access- and refresh-token.')
        url = f"{self.device_properties.host}/oidc/token"
        device_jwt = self.get_device_jwt()
        req_content = {
            "grant_type": grant_type,
            "client_id": self.device_properties.client_id,
            "client_assertion_type": "urn:ietf:params:oauth:client-assertion-type:jwt-bearer",
            "client_assertion": device_jwt['device_jwt'],
            "refresh_token": refresh_token
        }

        try:
            res = post(url, data=req_content)
            res.raise_for_status()
            return res.json()
        except ConnectionError as err:
            log.error("Connection to {} failed.".format(url))
            raise err
        except Exception as err:
            log.error(err)
            raise err
