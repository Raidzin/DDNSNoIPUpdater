from time import sleep

import httpx

import settings
from logs import (
    logger,
    SUCCESSFUL_IP_GET,
    SUCCESSFUL_IP_UPDATE,
    ERROR_IP_GET,
    ERROR_IP_UPDATE,
)

NOIP_URL = (
    'http://username:password@dynupdate.no-ip.com/nic/update'
    '?hostname={host}&myip={ip}'
)
STARTUP = 'APPLICATION_STARTUP'
SHUTDOWN = 'APPLICATION_SHUTDOWN'
INCORRECT_STATUS = 'Get incorrect status code'
SUCCESS_RESPONSE = 200


def get_ip_address() -> str:
    response = httpx.get(settings.IP_GETTER_URL)
    logger.info(
        event=SUCCESSFUL_IP_GET,
        status=response.status_code,
        response=response.text,
    )
    if response.status_code != SUCCESS_RESPONSE:
        raise httpx.HTTPError(message=INCORRECT_STATUS)
    return response.text


def update_ip(new_ip: str):
    response = httpx.post(
        url=NOIP_URL.format(
            ip=new_ip,
            host=settings.NOIP_HOSTNAME,
        ),
        auth=httpx.BasicAuth(
            username=settings.NOIP_USERNAME,
            password=settings.NOIP_PASSWORD,
        )
    )
    if response.status_code != 200:
        logger.error(
            event=ERROR_IP_UPDATE,
            error=INCORRECT_STATUS,
        )
        return
    logger.info(
        event=SUCCESSFUL_IP_UPDATE,
        status=response.status_code,
        response=response.text,
    )


def get_and_update_ip():
    try:
        update_ip(get_ip_address())
    except httpx.HTTPError as error:
        logger.error(
            event=ERROR_IP_GET,
            error=str(error),
        )


if __name__ == '__main__':
    logger.info(event=STARTUP)
    try:
        while True:
            get_and_update_ip()
            sleep(settings.INTERVAL)
    except KeyboardInterrupt:
        logger.info(event=SHUTDOWN)
