import json

from aiohttp import ClientSession

from src import config


async def send_logs(result: dict, send_errors: bool = config.LOG_DEAD):
    """Sends logs to every logstash endpoint in config
    :param result: JSON to send
    :param send_errors: indicating to send dead targets"""
    async with ClientSession() as session:
        if not send_errors and not result.get('status'):
            return
        for endpoint in config.LOGSTASH_ENDPOINTS:
            await session.post(endpoint, data=json.dumps(result))
