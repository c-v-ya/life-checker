import re

from src import config
from src.logger import send_logs


async def head(url, session):
    """Performs HEAD request to url and returns response headers or error"""
    try:
        async with session.head(url, ssl=config.USE_TLS) as response:
            return response.headers

    except Exception as err:
        return err


async def check(addr: str, port: int, session):
    """Performs request and checks if addr is alive"""
    response = await head(f'http://{addr}:{port}', session)
    result_dict = {
        'host': addr,
        'port': port,
        'status': False,
        'tls': config.USE_TLS,
    }

    if isinstance(response, Exception):
        status_text = f'{response.__class__.__name__}: can not connect to host'
        result_dict['status_text'] = status_text

        return result_dict

    result_dict['status'] = True
    result_dict['headers'] = {
        'date': [
            response.get('Date')
        ],
        'server': [
            response.get('Server')
        ],
        'content_type': [
            response.get('Content-Type')
        ],
        'content_length': [
            response.get('Content-Length')
        ]
    }

    await send_logs(result_dict)


def is_cidr(host_name):
    """Checks if host_name is a CIDR notation"""
    return re.match(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}/\d{1,2}.*', host_name)
