import os

from dotenv import load_dotenv
from logs import logger

load_dotenv()

LOGGER_NAME = 'ddns_updater'

_REQUIRED_ENVS = (
    'NOIP_USERNAME',
    'NOIP_PASSWORD',
    'NOIP_HOSTNAME',
)

__errors = False
for env in _REQUIRED_ENVS:
    if os.getenv(env) is None:
        logger.critical(event='ERROR_GET_ENV', env_name=env)
        __errors = True
if __errors:
    exit()

NOIP_USERNAME = os.getenv('NOIP_USERNAME')
NOIP_PASSWORD = os.getenv('NOIP_PASSWORD')
NOIP_HOSTNAME = os.getenv('NOIP_HOSTNAME')

IP_GETTER_URL = os.getenv('IP_GETTER_URL', default='https://ident.me')
INTERVAL = int(os.getenv('INTERVAL', default=300))
