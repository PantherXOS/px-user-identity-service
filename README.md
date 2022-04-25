# PantherX User Identity Service

- Provides signed response from `px-device-identity` via REST API
- runs on `127.0.0.1:8010`

## Setup

### Setup on PantherX

- (1) Setup, and register your device with `px-device-identity`
- (2) Add service to system configuration

```scheme
(service px-user-identity-service-type)
```

### Install with pip package manager

_Install these packages as root; Minimum python version: v3.7; Recommended: v3.8+_

```bash
# You should first install px-device-identity
# pip3 install https://source.pantherx.org/px-device-identity_latest.tgz
pip3 install https://source.pantherx.org/px-user-identity-service_latest.tgz
```

**Important**

1. This package depends on `px-device-identity`. We installed (or updated) this just now.
2. This computer should be registered using `px-device-identity` before running `px-user-identity-service`

## Run

This service only runs under `root`.

```bash
px-user-identity-service
```

### Run as Service

- PantherX OS: `herd start px-user-identity`
- systemd based distributions like Debian, Centos, use the service from [here](docs/systemd-service.md)

## Use Rest API

### QR Authentication

To request a QR authentication grant do:

_The service automatically determines required key security from config._

```bash
$ curl http://localhost:8010/auth/qr
{"auth_req_id": "f0943360-d6ef-4f07-8a20-8f5571818bd2", "exp": 300}
```

Next: Generate a QR code from `{ auth_req_id: '...', deviceId: '...' }`

To request a QR authentication grant status do:

```bash
$ curl http://localhost:8010/auth/qr/f0943360-d6ef-4f07-8a20-8f5571818bd2
{"status": "pending", "deviceId": "a174abd9-c9c0-4edb-a159-8892ab7fc47f"}
```

Next: Once the login has been approved, this response will contain the user `access_token`.

### BC Authentication

To request a BC authentication, post the username like to:

```bash
$ curl -X POST -H "Content-Type: application/json" \
-d '{"login_hint_token": "master.user-748@OnesDiD0"}' \
http://localhost:8010/auth/bc

{"auth_req_id": "280e04bb-4330-4dfc-ad26-8ebdde606be1", "expires_in": 600, "interval": 5}
```

Alternatively, to send a login message along with the request:

_This message will be shown on the user mobile phone_

```bash
curl -X POST -H "Content-Type: application/json" \
-d '{"login_hint_token": "master.user-748@OnesDiD0", "login_message": "Authorize login to OnesPHR"}' \
http://localhost:8010/auth/bc

{"auth_req_id": "26539b4d-ec85-42a1-9c21-716025e9da67", "expires_in": 600, "interval": 5}
```

To request the BC login status do:

```bash
$ curl http://localhost:8010/auth/bc/d179d4e7-96a3-417d-8bd1-35e6b7883080
{"message": "authorization_pending", "status": "pending"}
```

## Use as Library

_Note that this is only useful for applications intended to be run under `root`._

### QR Authentication

```python
from px_user_identity_service import QRAuthentication
qr = QRAuthentication()
# LOGIN
login_res = qr.login()
# Status
status_res = qr.status(login_res['auth_req_id])
```

### BC Authentication

```python
from px_user_identity_service import CIBAAuthentication
ciba = CIBAAuthentication()
# LOGIN
login_res = ciba.login(login_hint_token, login_message)
# Status
status_res = ciba.status(login_res['auth_req_id])
```

## Troubleshooting

Find logs at `/var/log/`

## Development

Create a guix environment like so:

```bash
guix shell --pure --check python tpm2-tss tpm2-tss-engine
python3 -m venv venv
source venv/bin/activate
pip3 install https://source.pantherx.org/px-device-identity_latest.tgz
pip3 install .
```

Create a package to manually install `px-device-identity`:

```bash
python3 setup.py sdist --format=tar
pip install px-device-identity-0.*.*.tar
```
