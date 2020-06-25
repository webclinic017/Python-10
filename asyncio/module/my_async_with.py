'''
THis is a simple implementation about pyhton async context manager.

Author : Minwook Je

$ python my_async_with.py

..........Enter Context..........

H e l l o   W o r l d !

..........Exit Context..........

'''

import asyncio
import sys


class AsyncContextManager:
    """Simple implementation about async with(async context manager)"""

    def __init__(self, msg):
        self.msg = msg

    async def __aenter__(self):
        await log("Enter Context")
        print()
        return self

    async def __aexit__(self, *args):
        print()
        await log("Exit Context")


async def log(msg, count=10, wait='.'):
    """Print message by an character & asleep with .1 per char"""

    for i in range(count * 2 + 1):
        if i == count:
            for char in msg:
                sys.stdout.write(char)
                sys.stdout.flush()
        else:
            sys.stdout.write(wait)
            sys.stdout.flush()

        await asyncio.sleep(.1)
    sys.stdout.write('\n')
    sys.stdout.flush()


async def main(message="Hello World!"):
    """Test Async Context Manager"""
    async with AsyncContextManager(message) as c:
        for m in c.msg:
            print(m, end=' ')
        print()


if __name__ == '__main__':
    asyncio.run(main("Hello World!"))
