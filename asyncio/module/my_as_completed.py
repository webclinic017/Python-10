import asyncio
from typing import List


def my_as_completed(coros: List):
    """
    It is roughly acting like as_completed() which is python's Built-in method.
    but Note that it's input type is not awaitable iterator but coroutine-list ( returns an iterator )
    """

    assert isinstance(coros, List)
    futures = [asyncio.create_task(coro) for coro in coros]

    async def first_to_finish():
        """
        A coroutine that waits for one of the futures
        to finish and then returns its result.
        """

        while True:
            # Give up control to the scheduler
            await asyncio.sleep(0)

            for future in futures:
                if future.done():
                    futures.remove(future)
                    return future.result()  # 코루틴 종료

    while len(futures) > 0:
        yield first_to_finish()


async def mycoro(number):
    print("Starting %d" % number)
    await asyncio.sleep(1.0 / number)
    print("Finishing %d" % number)
    return str(number)


async def print_when_done(tasks):
    for res in my_as_completed(tasks):
        print("Result %s" % await res)


if __name__ == '__main__':
    coros = [mycoro(i) for i in range(1, 101)]
    loop = asyncio.get_event_loop()
    loop.run_until_complete(print_when_done(coros))
    loop.close()
