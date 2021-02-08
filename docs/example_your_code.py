# https://docs.python.org/3/library/asyncio-task.html
import asyncio
import time


async def say_after(index: int, delay: int, what: str) -> None:
    print(f"started Task_{index} at {time.strftime('%X')} for {delay} sec.")
    await asyncio.sleep(delay)
    print(what)


async def main():
    simple_start = time.time()
    print(f"started at {time.strftime('%X')}")

    somedict = {3: 'hello',
                4: 'world'}
    i = 0
    for k, v in somedict.items():
        task = asyncio.create_task(say_after(i, k, v))
        await task
        i += 1
    print(f"finished Main at {time.strftime('%X')}")
    print(f'duration: {round(time.time()-simple_start, 5)}')
    print(f"finished at {time.strftime('%X')}")

asyncio.run(main())

# region OUTPUT
# started at 00:52:14
# started Task_0 at 00:52:14 for 3 sec.
# hello
# started Task_1 at 00:52:17 for 4 sec.
# world
# finished Main at 00:52:21
# duration: 7.00495   <-- При таком способе формирования Task выполняются последовательно, не конкурентно,
#                         поэтому время исполения суммируется
# finished at 00:52:21
# endregion
