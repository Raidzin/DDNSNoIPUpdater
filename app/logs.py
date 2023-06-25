import structlog
from structlog.processors import (
    add_log_level,
    TimeStamper,
    UnicodeDecoder,
    JSONRenderer
)

SUCCESSFUL_IP_GET = 'GET_IP_SUCCESS'
SUCCESSFUL_IP_UPDATE = 'UPDATE_IP_SUCCESS'
ERROR_IP_GET = 'GET_IP_ERROR'
ERROR_IP_UPDATE = 'UPDATE_IP_ERROR'

LOG_TIMESTAMP_FORMAT = '%d.%m.%Y %H:%M:%S.%f'

structlog.configure(
    processors=[
        add_log_level,
        TimeStamper(fmt=LOG_TIMESTAMP_FORMAT, utc=False),
        UnicodeDecoder(),
        JSONRenderer(),
    ],
)

logger = structlog.get_logger()
