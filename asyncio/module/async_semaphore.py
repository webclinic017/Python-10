"""
To Practice async tasks with semaphore, Event and Producer & Consumer pattern.

Author : Minwook Je
"""

import asyncio
from random import uniform, randrange
from typing import List
from collections import deque

queue = deque([])
log = lambda color, ms: print(COLORS[color] + ms)

COLORS = {
    "YELLOW": "\033[1;33m",
    "LIGHT_RED": "\033[1;31m",
    "LIGHT_BLUE": "\033[1;34m",
    "LIGHT_PURPLE": "\033[1;35m",
    "LIGHT_CYAN": "\033[1;36m",
    "LIGHT_GREEN": "\033[1;32m"
}


async def before_lock(color, name):
    """Before get Semaphore key, Do this job"""
    for i in range(4):
        log(color, f'Before Lock: {name} doing {i}')
        await asyncio.sleep(uniform(0.1, 0.5))


async def producer(ev: asyncio.Event, sema: asyncio.Semaphore,
                   name='producer', color="LIGHT_GREEN"):
    """
    It Creates elements infinitely.
    Also It informs to workers which got semaphore that "It's time to Consume" with event.clear(), event.set().
    """

    delay = uniform(0.1, 1.6)
    while True:
        log(color, 'prepare...')
        await asyncio.sleep(delay)

        log(color, 'ev.clear()')
        ev.clear()  # flag to false

        for _ in range(10):
            queue.appendleft(randrange(1, 100))

        await asyncio.sleep(delay)
        log(color, f'ev.set() >>> {queue}')
        ev.set()


async def worker(ev: asyncio.Event, sema: asyncio.Semaphore,
                 name='worker', color='YELLO'):
    """
    It consumes Element from queue if worker acquires semaphore.
    If not, do before_lock().
    """

    delay = 0.1
    data: List[int] = []

    for _ in range(3):
        await before_lock(color, name)

        async with sema:
            for _ in range(2):
                log(color, f'Get Semaphore: {name}')
                await ev.wait()  # Blocked until producer call ev.set()
                r = queue.pop()
                data.append(r)
                log(color, f'Data: {data}')
                await asyncio.sleep(delay)
    return data


async def main(sema_count=2, worker_count=6):
    semaphore = asyncio.Semaphore(sema_count)
    event = asyncio.Event()

    task = asyncio.create_task(producer(event, semaphore))  # 스케쥴 포함
    coros = [worker(event, semaphore, name=f'WORKER{i + 1:02d}', color=color)
             for i, color in zip(range(worker_count), COLORS.keys())]

    # 완료된 Worker
    for data in asyncio.as_completed(coros):
        try:
            await data
        except IndexError as e:
            print("<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<  All Consumed!  >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")

    # Producer 중지
    try:
        await asyncio.wait_for(task, 1)
    except asyncio.TimeoutError:
        print("asyncio.TimeoutError")
    finally:
        print("END")


if __name__ == '__main__':
    asyncio.run(main())
