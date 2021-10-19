from src import config


async def head(url, session):
    """Performs HEAD request to url and returns response headers or error"""
    try:
        return (await session.head(url, ssl=config.USE_TLS)).headers
    except Exception as err:
        return err


async def check(addr: str, port: int, session):
    """Performs request and checks if addr is alive"""
    response = await head(f'https://{addr}:{port}', session)

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
        'date': [response.get('Date')],
        'server': [response.get('Server')],
        'content_type': [response.get('Content-Type')],
        'content_length': [response.get('Content-Length')],
    }

    return result_dict
