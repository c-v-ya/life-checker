import asyncio
import contextlib
import ipaddress

from src import config
from src.checker import check
from src.logger import send_logs

BUFFER = []  # buffering results before sending them
BUFFER_LIMIT = 10000


async def worker(queue: asyncio.Queue):
    while True:
        result = await queue.get()
        BUFFER.append(result)
        if len(BUFFER) >= BUFFER_LIMIT:
            await send_logs(BUFFER)
            BUFFER.clear()

        queue.task_done()


async def run():
    with open(config.TARGETS_FILE, 'r') as f:
        targets = f.read().splitlines()

    tasks = asyncio.Queue()

    for target in targets:
        host_name, port = target.split(':')
        try:
            cidr = ipaddress.IPv4Network(host_name)
        except ValueError:
            cidr = [host_name]

        for host_ip in cidr:
            task = asyncio.create_task(
                check(str(host_ip), port)
            )
            await tasks.put(task)

    workers = [asyncio.create_task(worker(tasks)) for _ in range(10)]
    await tasks.join()

    for task in workers:
        task.cancel()
        with contextlib.suppress(asyncio.CancelledError):
            await task

    await send_logs(BUFFER)  # sending last batch of results


if __name__ == '__main__':
    asyncio.run(run())
