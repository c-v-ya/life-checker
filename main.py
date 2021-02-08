import asyncio
import ipaddress

from aiohttp import ClientSession, ClientTimeout

from src import config
from src.checker import is_cidr, check


async def run():
    with open(config.TARGETS_FILE, 'r') as f:
        targets = f.read().splitlines()

    timeout = ClientTimeout(total=config.RESPONSE_TIMEOUT)

    async with ClientSession(timeout=timeout) as session:
        for target in targets:
            host_name, port = target.split(':')
            if is_cidr(host_name):
                # посмотри пожалуйста директорию docs
                for host_ip in ipaddress.IPv4Network(host_name):
                    task = asyncio.create_task(
                        check(str(host_ip), port, session)
                    )
                    await task
            else:
                task = asyncio.create_task(
                    check(host_name, port, session)
                )
                await task


if __name__ == '__main__':
    asyncio.run(run())
