import asyncio

from aiohttp import ClientTimeout, ClientSession

from src import config

TIMEOUT = ClientTimeout(total=config.RESPONSE_TIMEOUT)


async def head(url):
    """Performs HEAD request to url and returns response headers or error"""
    try:
        async with ClientSession(timeout=TIMEOUT) as session:
            async with session.head(url, ssl=config.USE_TLS) as response:
                return response.headers

    except Exception as err:
        return err


async def check(addr: str, port: int):
    """Performs request and checks if addr is alive"""
    response = await head(f'http://{addr}:{port}')

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

    return result_dict
