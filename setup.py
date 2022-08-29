import pathlib
from setuptools import setup, find_packages

HERE = pathlib.Path(__file__).parent

VERSION = '0.0.7'
PACKAGE_NAME = 'px-user-identity-service'
AUTHOR = 'Franz Geffke'
AUTHOR_EMAIL = 'franz@pantherx.org'
URL = 'https://git.pantherx.org/development/applications/px-user-identity-service'

LICENSE = 'MIT'
DESCRIPTION = 'User Identity API to support QR and BC login with device signature.'
LONG_DESCRIPTION = (HERE / "README.md").read_text()
LONG_DESC_TYPE = "text/markdown"

INSTALL_REQUIRES = [
    'requests',
    'falcon',
    'px-device-identity',
    'waitress'
]

setup(
    name=PACKAGE_NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type=LONG_DESC_TYPE,
    author=AUTHOR,
    license=LICENSE,
    author_email=AUTHOR_EMAIL,
    url=URL,
    install_requires=INSTALL_REQUIRES,
    entry_points={
        'console_scripts': ['px-user-identity-service=px_user_identity_service.main:main'],
    },
    packages=find_packages(),
    zip_safe=False
)
