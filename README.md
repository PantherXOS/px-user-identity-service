# PantherX User Identity Service

- Provides signed response from `px-device-identity` via REST API
- runs on `127.0.0.1:8019`

## Setup

```bash
python3 -m venv venv
source venv/bin/activate
pip install .
```

### Install with pip package manager

```bash
pip3 install https://source-git-pantherx-org.s3.eu-central-1.amazonaws.com/px-user-identity-service_latest.tgz
```

## Run

This service only runs under `root`.

```bash
px-user-identity-service
```

## Use Rest API

To request a QR authentication grant do:

_The service automatically determines required key security from config._

```bash
$ curl http://localhost:8010/auth/qr
{"auth_req_id": "f0943360-d6ef-4f07-8a20-8f5571818bd2", "exp": 300}
```

To request a QR authentication grant status do:

```bash
$ curl http://localhost:8010/auth/qr/f0943360-d6ef-4f07-8a20-8f5571818bd2
{"status": "pending", "deviceId": "a174abd9-c9c0-4edb-a159-8892ab7fc47f"}
```

## Troubleshooting

Find logs at `/var/log/`

## Development

Create a guix environment like so:

```bash
guix environment \
--pure python \
--ad-hoc python-idna python-requests python-authlib-0.14.3 python-exitstatus-2.0.1 \
python-pycryptodomex python-jose python-pyyaml-v5.3.1 python-shortuuid-v1.0.1 \
python-appdirs tpm2-tss tpm2-tss-engine python-setuptools python-psutil
```

Create a package to manually install `px-device-identity`:

```bash
python3 setup.py sdist --format=tar
pip install px-device-identity-0.*.*.tar
```