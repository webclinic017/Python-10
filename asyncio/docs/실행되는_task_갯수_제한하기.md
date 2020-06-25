# 실행되는 Tasks들의 갯수 제한하기
> [번역 자료](https://www.artificialworlds.net/blog/2017/05/31/python-3-large-numbers-of-tasks-with-limited-concurrency/)

`.as_completed()`든 `.gather()`을 사용할때, Event-loop에서 실행되는 Task들의 갯수를 제한하고 싶은 경우가 있다.
해당 자료는 이에 대한 방법을 제시한다.

목표 

- large numbers of tasks with limited concurrency

- running very large numbers of tasks with limited concurrency

아래의 코드는 일반적으로 동작하는 `.as_completed()`를 사용한 테스트 코드이다.
```python
async def mycoro(number):
    print("Starting %d" % number)
    await asyncio.sleep(1.0 / number)
    print("Finishing %d" % number)
    return str(number)

async def print_when_done(tasks):
    for res in asyncio.as_completed(tasks):
        print("Result %s" % await res)


if __name__ == '__main__':
    coros = [mycoro(i) for i in range(1, 101)]
    loop = asyncio.get_event_loop()
    loop.run_until_complete(print_when_done(coros))
    loop.close()
```

## `as_completed()` 구현하기
> 위와 같이 동작하는 as_completed()를 구현한다.

```python

import asyncio
def my_as_completed(coros):
    """
    It is roughly acting sames as as_completed()
    but Note this is not a coroutine ( returns an iterator )
    """

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
```

테스트 코드

```python
async def print_when_done(tasks):
    for res in my_as_completed(tasks):
        print("Result %s" % await res)
```

실행시켜 보면 built-in .as_completed()와 같이 동작하는 것을 알 수 있다.

## Tasks의 갯수를 제한하는 `as_completed()`
> `.islice()`

./module/limited_as_completed.py
```python
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
    loop = asyncio.get_event_loop()
    loop.run_until_complete(print_when_done(coros))
    loop.close()

```

- 10개 단위(limit)로 tasks들이 동작하는 것을 볼 수 있다. 

## Task 갯수 제한하기 2
> Semaphore



## next step

- [asyncio.semaphore in async-await function](https://stackoverflow.com/questions/40836800/python-asyncio-semaphore-in-async-await-function)
- [Making 100 million requests with Python aiohttp](https://www.artificialworlds.net/blog/2017/06/12/making-100-million-requests-with-python-aiohttp/)
- [Making 1 million requests with python-aiohttp](https://pawelmhm.github.io/asyncio/python/aiohttp/2016/04/22/asyncio-aiohttp.html)
- [Adding a concurrency limit to Python’s asyncio.as_completed](https://www.artificialworlds.net/blog/2017/06/27/adding-a-concurrency-limit-to-pythons-asyncio-as_completed/)
      
