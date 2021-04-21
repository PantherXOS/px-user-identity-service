import pathlib
from setuptools import setup, find_packages

HERE = pathlib.Path(__file__).parent

VERSION = '0.0.1'
PACKAGE_NAME = 'px-user-identity-service'
AUTHOR = 'Franz Geffke'
AUTHOR_EMAIL = 'franz@pantherx.org'
URL = 'https://git.pantherx.org/development/applications/px-user-identity-service'

LICENSE = ''
DESCRIPTION = 'Provides access to device signing capabilities via REST API.'
LONG_DESCRIPTION = (HERE / "README.md").read_text()
LONG_DESC_TYPE = "text/markdown"

INSTALL_REQUIRES = [
    'requests>=2.22.0,<2.30',
    'falcon<=2.2.0',
    'px-device-identity',
    'exitstatus>=2.0.1,<2.1',
    'pyyaml>=5.3.1,<5.4',
    'waitress>=1.1.0,<1.2'
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
    entry_points = {
        'console_scripts': ['px-user-identity-service=px_user_identity_service.main:main'],
    },
    packages=find_packages(),
    zip_safe=False
)
