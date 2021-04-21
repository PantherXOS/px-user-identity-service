import logging
from logging.handlers import RotatingFileHandler, SysLogHandler
from platform import system

opsys = system()


log = logging.getLogger('px_user_identity_service')
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s: %(message)s', "%Y-%m-%d %H:%M:%S")
formatter_cli = logging.Formatter('%(levelname)s: %(message)s')

log.setLevel(logging.DEBUG)

if opsys == 'Linux':
    import syslog

    # On Linux we log all events to file
    fh = RotatingFileHandler('/var/log/px-user-identity-service.log', maxBytes=10000, backupCount=1)
    fh.setLevel(logging.INFO)
    fh.setFormatter(formatter)
    log.addHandler(fh)

    #On Linux we engage syslog
    sh = SysLogHandler()
    sh.setLevel(logging.WARNING)
    sh.setFormatter(formatter)
    log.addHandler(sh)

ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
ch.setFormatter(formatter_cli)
log.addHandler(ch)
