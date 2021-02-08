# https://docs.python.org/3/library/asyncio-task.html

import asyncio
import time


async def say_after(index: int, delay: int, what: str) -> None:
    print(f"started Task_{index} at {time.strftime('%X')} for {delay} sec.")
    await asyncio.sleep(delay)
    print(what)


async def main():
    simple_start = time.time()
    print(f"started Main at {time.strftime('%X')}")
    task1 = asyncio.create_task(
        say_after(0, 3, 'hello'))

    task2 = asyncio.create_task(
        say_after(1, 4, 'world'))
    await task1
    await task2
    print(f"finished Main at {time.strftime('%X')}")
    print(f'duration: {round(time.time()-simple_start, 5)}')
asyncio.run(main())

# region OUTPUT
# started Main at 01:07:38
# started Task_0 at 01:07:38 for 3 sec. <- практически условно одновременно
# started Task_1 at 01:07:38 for 4 sec. <-
# hello
# world
# finished Main at 01:07:42
# duration: 4.00163
# endregion
