# server.py
"""

$ bash timed.sh python client-async-sem.py 10000
    server.py:15: DeprecationWarning: Application.make_handler(...) is deprecated, use AppRunner API instead
      app.make_handler(), '127.0.0.1', 8080)
    Memory usage: 71068KB	Time: 19.10 seconds	CPU usage: 70%
"""

from aiohttp import web
import asyncio
import random

async def handle(request):
    await asyncio.sleep(random.randint(0, 3))
    return web.Response(text="Hello, World!")

async def init():
    app = web.Application()
    app.router.add_route('GET', '/{name}', handle)
    return await loop.create_server(
        app.make_handler(), '127.0.0.1', 8080)

loop = asyncio.get_event_loop()
loop.run_until_complete(init())
loop.run_forever()