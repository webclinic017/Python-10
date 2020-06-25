import asyncio
from itertools import islice
from typing import Generator, Awaitable


def limited_as_completed(coros: Generator[Awaitable, None, None], limit):
    """
    It limits number of tasks and act like .as_completed()
    but Note this is not a coroutine ( returns an iterator )
    """
    assert isinstance(coros, Generator)

    # limits number of tasks
    tasks = [asyncio.create_task(coro)
             for coro in islice(coros, 0, limit)]

    async def first_to_finish():
        """
        A coroutine that waits for one of the futures
        to finish and then returns its result.
        """

        while True:
            # Give up control to the scheduler
            await asyncio.sleep(0)

            for task in tasks:
                if task.done():
                    # consume
                    tasks.remove(task)
                    try:
                        # producer
                        newt = next(coros)
                        tasks.append(asyncio.create_task(newt))
                    except StopIteration as e:
                        pass
                    return task.result()

    # keep limit number of tasks
    while len(tasks) > 0:
        yield first_to_finish()


async def mycoro(number):
    print("Starting %d" % number)
    await asyncio.sleep(1.0 / number)
    print("Finishing %d" % number)
    return str(number)


async def print_when_done(tasks):
    for res in limited_as_completed(tasks, 10):
        print("Result %s" % await res)


if __name__ == '__main__':
    coros = (mycoro(i) for i in range(1, 101))  # Generator를 준다.
    asyncio.run(print_when_done(coros))
