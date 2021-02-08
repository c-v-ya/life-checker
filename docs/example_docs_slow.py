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
    await say_after(0, 3, 'hello')
    await say_after(1, 4, 'world')
    print(f"finished Main at {time.strftime('%X')}")
    print(f'duration: {round(time.time()-simple_start, 5)}')
asyncio.run(main())

# region OUTPUT
# started Main at 00:51:36
# started Task_0 at 00:51:36 for 3 sec.
# hello
# started Task_1 at 00:51:39 for 4 sec.
# world
# finished Main at 00:51:43
# duration: 7.00484
# endregion
