import asyncio
import ipaddress

from aiohttp import ClientSession, ClientTimeout

from src import config
from src.checker import check
from src.logger import send_logs

BUFFER = []  # buffering results before sending them
BUFFER_LIMIT = 10000
TIMEOUT = ClientTimeout(total=config.RESPONSE_TIMEOUT)


async def run():
    with open(config.TARGETS_FILE, 'r') as f:
        targets = f.read().splitlines()

    tasks = []
    session = ClientSession(timeout=TIMEOUT)

    for target in targets:
        host_name, port = target.split(':')
        try:
            cidr = ipaddress.IPv4Network(host_name)
        except ValueError:
            cidr = [host_name]

        for host_ip in cidr:
            tasks.append(
                asyncio.create_task(check(str(host_ip), port, session))
            )

    for task in tasks:
        result = await task
        BUFFER.append(result)
        if len(BUFFER) >= BUFFER_LIMIT:
            await send_logs(BUFFER)
            BUFFER.clear()

    await session.close()
    await send_logs(BUFFER)  # sending last batch of results


if __name__ == '__main__':
    asyncio.run(run())
