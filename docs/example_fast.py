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
    # region version 1 - создание списка задач и выполение их условно-одновременно-конкурентно
    i = 0
    tasks = []
    for k, v in somedict.items():
        task = asyncio.create_task(say_after(i, k, v))
        tasks.append(task)
        i += 1
    for task in tasks:
        await task
    # endregion

    # region version 2 - создание списка корутин и выполение условно-одновременно-конкурентно
    # coroutines = []
    # for k, v in somedict.items():
    #     coroutines.append(say_after(i, k, v))
    #     i += 1
    # await asyncio.gather(*coroutines)
    # endregion

    print(f"finished Main at {time.strftime('%X')}")
    print(f'duration: {round(time.time() - simple_start, 5)}')
    print(f"finished at {time.strftime('%X')}")
asyncio.run(main())

# region OUTPUT - version 1
# started at 00:54:23
# started Task_0 at 00:54:23 for 3 sec. <- практически условно одновременно
# started Task_1 at 00:54:23 for 4 sec. <-
# hello
# world
# finished Main at 00:54:27
# duration: 4.00172 <-- При таком способе формирования Task выполняются конкурентно
#                       поэтому время исполения, условно, по максимально долгой Таске
# finished at 00:54:27

# условное аналогично при коде в версии 2
# region OUTPUT - version 2
# started at 00:59:04
# started Task_0 at 00:59:04 for 3 sec.
# started Task_1 at 00:59:04 for 4 sec.
# hello
# world
# finished Main at 00:59:08
# duration: 4.00206
# finished at 00:59:08