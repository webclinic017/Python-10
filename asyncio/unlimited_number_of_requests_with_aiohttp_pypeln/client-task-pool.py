# bash timed.sh python client-my-taskpool.py 1000
import asyncio
import sys
from aiohttp import ClientSession, TCPConnector


class TaskPool(object):

    def __init__(self, workers):
        self._semaphore = asyncio.Semaphore(workers)
        self._tasks = set()

    async def put(self, coro):
        await self._semaphore.acquire()

        task = asyncio.ensure_future(coro)
        self._tasks.add(task)
        task.add_done_callback(self._on_task_done)

    def _on_task_done(self, task):
        self._tasks.remove(task)
        self._semaphore.release()

    async def join(self):
        await asyncio.gather(*self._tasks)

    async def __aenter__(self):
        return self

    def __aexit__(self, exc_type, exc, tb):
        return self.join()


limit = 1000


async def fetch(url, session):
    async with session.get(url) as response:
        return await response.read()


async def _main(url, total_requests):
    connector = TCPConnector(limit=None)
    async with ClientSession(connector=connector) as session, TaskPool(limit) as tasks:
        for i in range(total_requests):
            await tasks.put(fetch(url.format(i), session))


url = "http://localhost:8080/{}"
loop = asyncio.get_event_loop()
loop.run_until_complete(_main(url, int(sys.argv[1])))
