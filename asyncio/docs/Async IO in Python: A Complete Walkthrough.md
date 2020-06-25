# Async IO in Python: A Complete Walkthrough
> [Real Python](https://realpython.com/async-io-python/#async-ios-roots-in-generators)


## Sync vs Async

sync
```python
#!/usr/bin/env python3
# countsync.py

import time

def count():
    print("One")
    time.sleep(1)
    print("Two")

def main():
    for _ in range(3):
        count()

if __name__ == "__main__":
    s = time.perf_counter()
    main()
    elapsed = time.perf_counter() - s
    print(f"{__file__} executed in {elapsed:0.2f} seconds.")
```
```
One
Two
One
Two
One
Two
tmp.py executed in 3.00 seconds.
```

async
```python
#!/usr/bin/env python3
# countasync.py

import asyncio

async def count():
    print("One")
    await asyncio.sleep(1) # 명시적 context change
    print("Two")

async def main():
    await asyncio.gather(count(), count(), count())

if __name__ == "__main__":
    import time
    s = time.perf_counter()
    asyncio.run(main())
    elapsed = time.perf_counter() - s
    print(f"{__file__} executed in {elapsed:0.2f} seconds.")
```

```
One
One
One
Two
Two
Two
tmp.py executed in 1.00 seconds.

```

## The Rules of Async IO
> async, await

`async def`는 2가지 역할을 합니다. 1. native coroutine 생성 2. asynchronous generator를 생성

또한 키워드 `await`는 함수 제어를 이벤트 루프로 다시 전달합니다. ("내가 기다리는 모든 것의 결과가 반환 될 때까지 실행을 일시 중지 하고 Event Loop는 그동안 다른 일을 해보자.")

- `async def`의 블록 안에서는 await, return, yield를 사용가능합니다.
    - coroutine으로 사용할 때는 await, return을 사용합니다.
    - asynchronous generator로 사용할 경우에는 블록에서 `yield`를 사용합니다. 이때 `async for`를 사용하여 iterate 할 수 있습니다.    
    - async def안에서는 `yield from`을 사용할 수 없습니다. (SyntaxError)
    - 마찬가지로 일반 def 함수에서 await을 사용하면 SyntaxError
    
  
```python
# coroutine
async def f(x):
    y = await z(x)
    return y

# async generator
async def g(x):
    yield x
    
# SyntaxError    
async def m(x):
    yield from gen(x)

# SyntaxError
def m(x):
    y = await z(x)
```


추가로 `await f()`을 사용할 때, f()는 awaitable object입니다. 
`awaitable object`이란 1) Another Coroutine(Task, Coroutine, Future) 2) Object defining __await__()입니다.

또한 `@asyncio.coroutine`문법은 async/await(native coroutine)가 python 3.5에 등장하기 전까지 사용했던 `generator-based coroutine`방식으로, python 3.10 버전에서는 사라질 예정입니다.
```python
import asyncio

@asyncio.coroutine
def py34_coro():
    """Generator-based coroutine, older syntax"""
    yield from stuff()

async def py35_coro():
    """Native coroutine, modern syntax"""
    await stuff()
```

다음 코드는 random하게 i를 만들면서 만약 `threshold`와 i가 같으면 중지하는 코루틴들을 보여주는 코드입니다.
이를 통해 전반적인 asyncio의 동작을 확인 할 수 있다.
```python
#!/usr/bin/env python3
# rand.py

import asyncio
import random

# ANSI colors
c = (
    "\033[0m",  # End of color
    "\033[36m",  # Cyan
    "\033[91m",  # Red
    "\033[35m",  # Magenta
)


async def makerandom(idx: int, threshold: int = 6) -> int:
    print(c[idx + 1] + f"Initiated makerandom({idx}).")
    i = random.randint(0, 10)
    while i <= threshold:
        print(c[idx + 1] + f"makerandom({idx}) == {i} too low; retrying.")
        await asyncio.sleep(idx + 1)
        i = random.randint(0, 10)
    print(c[idx + 1] + f"---> Finished: makerandom({idx}) == {i}" + c[0])
    return i


async def main():
    res = await asyncio.gather(*(makerandom(i, 10 - i - 1) for i in range(3)))
    return res


if __name__ == "__main__":
    random.seed(444)
    r1, r2, r3 = asyncio.run(main())
    print()
    print(f"r1: {r1}, r2: {r2}, r3: {r3}")

```

![](./img/asyncio.png)

결과를 보면 idx의 크기에 따라 sleep 시간을 길게두어 `Cyan`이 가장 높은 context change 권한을 가졌던것을 볼 수 있다.
참고로 이야기 하면, 위의 코드는 single thread에서(엄밀하게는 main에서 동작하는 EventLoop thread도 존재할 것같다. node.js처럼) 코루틴들에 대해 권한을 바꿔가며 동작하는 concurrency한 코드이다.



## Async IO Design Patterns

### Chaining Coroutines
```python
#!/usr/bin/env python3
# chained.py

import asyncio
import random
import time


async def part1(n: int) -> str:
    i = random.randint(0, 10)
    print(f"part1({n}) sleeping for {i} seconds.")
    await asyncio.sleep(i)
    result = f"result{n}-1"
    print(f"Returning part1({n}) == {result}.")
    return result


async def part2(n: int, arg: str) -> str:
    i = random.randint(0, 10)
    print(f"part2{n, arg} sleeping for {i} seconds.")
    await asyncio.sleep(i)
    result = f"result{n}-2 derived from {arg}"
    print(f"Returning part2{n, arg} == {result}.")
    return result


async def chain(n: int) -> None:
    start = time.perf_counter()
    p1 = await part1(n) # 다 끝날때까지 내려가지 않는다.
    p2 = await part2(n, p1)
    end = time.perf_counter() - start
    print(f"-->Chained result{n} => {p2} (took {end:0.2f} seconds).")


async def main(*args) -> None:
    # def gather(*coros_or_futures) unpacking 해서 주어야한다.
    await asyncio.gather(*(chain(arg) for arg in args))


if __name__ == "__main__":
    import sys

    random.seed(444)
    args = [1, 2, 3] if len(sys.argv) == 1 else map(int, sys.argv[1:])
    start = time.perf_counter()
    asyncio.run(main(*args))
    end = time.perf_counter() - start
    print(f"Program finished in {end:0.2f} seconds.")

```

```
$ python tmp.py 9 6 3
part1(9) sleeping for 4 seconds.
part1(6) sleeping for 4 seconds.
part1(3) sleeping for 0 seconds.
Returning part1(3) == result3-1.
part2(3, 'result3-1') sleeping for 4 seconds.
Returning part1(9) == result9-1.
part2(9, 'result9-1') sleeping for 7 seconds.
Returning part1(6) == result6-1.
part2(6, 'result6-1') sleeping for 4 seconds.
Returning part2(3, 'result3-1') == result3-2 derived from result3-1.
-->Chained result3 => result3-2 derived from result3-1 (took 4.00 seconds).
Returning part2(6, 'result6-1') == result6-2 derived from result6-1.
-->Chained result6 => result6-2 derived from result6-1 (took 8.00 seconds).
Returning part2(9, 'result9-1') == result9-2 derived from result9-1.
-->Chained result9 => result9-2 derived from result9-1 (took 11.01 seconds).
Program finished in 11.01 seconds.

```

`asyncio.gatherㄴ(*aws, loop=None, return_exceptions=False)`

- 결괏값의 순서는 aws에 있는 어웨이터블의 순서와 일치합니다.
- `return_exceptions`는 default로 `False`이며,  `aws 시퀀스`의 다른 어웨이터블은 취소되지 않고 계속 실행됩니다.

### Using a Queue

```python
import asyncio
import itertools as it
import os
import random
import time


async def makeitem(size: int = 5) -> str:
    return os.urandom(size).hex()


async def randsleep(p: int = None, b: int = 5, caller=None) -> None:
    i = random.randint(0, 10)
    if p is not None:
        i = p
    if caller:
        print(f"{caller} sleeping for {i} seconds.")
    await asyncio.sleep(i)


async def produce(name: int, q: asyncio.Queue) -> None:
    n = random.randint(0, 10)
    # range() 사용하지 않는이유? it.repeat(None,n)이 더 빠르다.
    for _ in it.repeat(None, n):
        await randsleep(p=0, caller=f"Producer {name}")
        i = await makeitem()
        t = time.perf_counter()
        await q.put((i, t))
        print(f"Producer {name} added <{i}> to queue.")


async def consume(name: int, q: asyncio.Queue) -> None:
    while True:
        await randsleep(caller=f"Consumer {name}")
        i, t = await q.get()  # If queue is empty, wait until an item is available.
        now = time.perf_counter()
        print(f"Consumer {name} got element <{i}>"
              f" in {now - t:0.5f} seconds.")
        q.task_done()


async def main(nprod: int, ncon: int):
    q = asyncio.Queue()
    producers = [asyncio.create_task(produce(n, q)) for n in range(nprod)]
    consumers = [asyncio.create_task(consume(n, q)) for n in range(ncon)]
    await asyncio.gather(
        *producers)  # 모든 생산자가 생산을 마칠때까지 이 항목을 넘어갈 수 없다.(모든 Producer의 생산 보장, 생산을 마친 producer.cancel() 적용)
    print("Every Producer is Cancelled")
    await q.join()  # 생산자가 Queue.put해준 모든 item들이 처리가 될때까지 대기해준다.
    for c in consumers:  # 생산되기를 기다리는 Consumer cancel()
        c.cancel()


if __name__ == "__main__":
    import argparse

    random.seed(443)
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--nprod", type=int, default=5)
    parser.add_argument("-c", "--ncon", type=int, default=10)
    ns = parser.parse_args()

    start = time.perf_counter()
    asyncio.run(main(**ns.__dict__))
    elapsed = time.perf_counter() - start
    print(f"Program completed in {elapsed:0.5f} seconds.")
```

```
Producer 0 sleeping for 0 seconds.
Producer 1 sleeping for 0 seconds.
Consumer 0 sleeping for 4 seconds.
Consumer 1 sleeping for 5 seconds.
Consumer 2 sleeping for 4 seconds.
Consumer 3 sleeping for 1 seconds.
Consumer 4 sleeping for 4 seconds.
Producer 0 added <c6d2c88ea9> to queue.
Producer 0 sleeping for 0 seconds.
Producer 1 added <d54c2ed91b> to queue.
Producer 1 sleeping for 0 seconds.
Producer 0 added <36fe862ec3> to queue.
Producer 1 added <67c90217e5> to queue.
Producer 1 sleeping for 0 seconds.
Producer 1 added <cbfca546cc> to queue.
Producer 1 sleeping for 0 seconds.
Producer 1 added <07e1fa7659> to queue.
Producer 1 sleeping for 0 seconds.
Producer 1 added <6a44169212> to queue.
Producer 1 sleeping for 0 seconds.
Producer 1 added <06c5237c7b> to queue.
Producer 1 sleeping for 0 seconds.
Producer 1 added <17c91b585d> to queue.
Producer 1 sleeping for 0 seconds.
Producer 1 added <e07a11a6bc> to queue.
Producer 1 sleeping for 0 seconds.
Producer 1 added <6b3e82c070> to queue.
Producer 1 sleeping for 0 seconds.
Producer 1 added <583fc960a8> to queue.
Every Producer is Cancelled         --> await asyncio.gather(*producer) is fin 
Consumer 3 got element <c6d2c88ea9> in 1.00150 seconds.
Consumer 3 sleeping for 3 seconds.
Consumer 0 got element <d54c2ed91b> in 4.00300 seconds.
Consumer 0 sleeping for 1 seconds.
Consumer 2 got element <36fe862ec3> in 4.00322 seconds.
Consumer 2 sleeping for 6 seconds.
Consumer 4 got element <67c90217e5> in 4.00337 seconds.
Consumer 4 sleeping for 7 seconds.
Consumer 3 got element <cbfca546cc> in 4.00348 seconds.
Consumer 3 sleeping for 9 seconds.
Consumer 1 got element <07e1fa7659> in 5.00186 seconds.
Consumer 1 sleeping for 7 seconds.
Consumer 0 got element <6a44169212> in 5.00334 seconds.
Consumer 0 sleeping for 3 seconds.
Consumer 0 got element <06c5237c7b> in 8.00663 seconds.
Consumer 0 sleeping for 7 seconds.
Consumer 2 got element <17c91b585d> in 10.00629 seconds.
Consumer 2 sleeping for 0 seconds.
Consumer 2 got element <e07a11a6bc> in 10.00646 seconds.
Consumer 2 sleeping for 5 seconds.
Consumer 4 got element <6b3e82c070> in 11.00492 seconds.
Consumer 4 sleeping for 10 seconds.
Consumer 1 got element <583fc960a8> in 12.00228 seconds.
Consumer 1 sleeping for 3 seconds.
Program completed in 12.00375 seconds.

```

코드들에 대해 설명을 하자면,

`i, t = await q.get()`는 queue가 비워져 있다면, wait until an item is available. 한다.

`Queue.join()`은 모든 생산된 task가 비워질때까지 기다려준다.

`await asyncio.gather(*producers)`은 모든 producer가 생산을 마칠때까지 await해준다. 즉 생산을 완료하기 전까진 아래 코드로 진행될 수 없다.
그렇기 때문에 위의 소스코드에서 Producer에 wait을 0을 주어, 실험해보았고 예상과 같은 결과가 도출되었다.
 
 
**추가적으로 range()보다 itertools를 사용해 for 도는 것이 더 빠르다**는 새로운 사실을 배웠다. 

```python
for _ in itertools.repeat(None, 10000):
    do_something()
```
This is faster than:
```python
for i in range(10000):
    do_something().
```
The former wins because all it needs to do is update the reference count for the existing None object. The latter loses because the range() or xrange() needs to manufacture 10,000 distinct integer objects.


## `async for`
> `Async Generators + Comprehensions`

`async for`은 iterator이다.
The purpose of an asynchronous iterator is for it to be able to call asynchronous code at each stage when it is iterated over.

해당 개념의 확장은 `asynchronous generator`이다. 
Using yield within a coroutine became possible in Python 3.6 (via PEP 525), 
which introduced `asynchronous generators` with the purpose of allowing await and yield to be used in the same coroutine function body:

```python
import asyncio


async def mygen(u: int = 10):
    """Yield powers of 2."""
    i = 0
    while i < u:
        yield 2 ** i
        i += 1
        print(i, "now sleep")
        await asyncio.sleep(0.1)


async def main():
    # This does not introduce concurrent execution
    # It is meant to show syntax only
    g = [i async for i in mygen()]
    f = [j async for j in mygen() if not (j // 3 % 5)]
    return g, f


g, f = asyncio.run(main())
print(g) 
print(f) 
```

```
1 now sleep
2 now sleep
3 now sleep
4 now sleep
5 now sleep
6 now sleep
7 now sleep
8 now sleep
9 now sleep
10 now sleep
1 now sleep
2 now sleep
3 now sleep
4 now sleep
5 now sleep
6 now sleep
7 now sleep
8 now sleep
9 now sleep
10 now sleep
[1, 2, 4, 8, 16, 32, 64, 128, 256, 512]
[1, 2, 16, 32, 256, 512]
```
결과를 보면 Event loop를 통해 비동기적으로 iterate하지 않고 동기적으로 첫번째 `async for`가 끝난 뒤, 다음 `async for`가 진행되었다.

다시말하면, `asynchronous iterators`와 `asynchronous generators`는 concurrently map some function over a sequence or iterator 하도록 설계되지 않았다.


원문을 추가하자면
```
This is a crucial distinction: neither asynchronous generators nor comprehensions make the iteration concurrent. 
All that they do is provide the look-and-feel of their synchronous counterparts,
but with the ability for the loop in question to give up control to the event loop for some other coroutine to run.

In other words, asynchronous iterators and asynchronous generators are not designed to concurrently map some function over a sequence or iterator. 
They’re merely designed to let the enclosing coroutine allow other tasks to take their turn. 
The async for and async with statements are only needed to the extent that using plain for or with would “break” the nature of await in the coroutine. 
This distinction between asynchronicity and concurrency is a key one to grasp.
```

## The Event Loop 와 asyncio.run()
> asyncio.run(), introduced in Python 3.7


1. Coroutines don’t do much on their own until they are tied to the event loop.
2. By default, an async IO event loop runs in a single thread and on a single CPU core.
    -  It is also possible to run event loops across multiple cores. Check out this [talk by John Reese](https://www.youtube.com/watch?v=0kXaLh8Fz3k&feature=youtu.be&t=10m30s) for more, and be warned that your laptop may spontaneously combust.
3. Event loops are pluggable. 즉 `uvloop`같은 오픈소스로 대체해서 사용도 가능하다.
    - asyncio 패키지의 event loop는 2가지 종류가 있다.
        1. class asyncio.SelectorEventLoop (unix, window)
        2. class asyncio.ProactorEventLoop (window용)
        3. class asyncio.AbstractEventLoop (인터페이스)
        
## A Full Program: Asynchronous Requests
> ./aiohttp

1. Read a sequence of URLs from a local file, urls.txt.

2. Send GET requests for the URLs and decode the resulting content. If this fails, stop there for a URL.

3. Search for the URLs within href tags in the HTML of the responses.

4. Write the results to foundurls.txt.

5. Do all of the above as asynchronously and concurrently as possible. 
    - (Use aiohttp for the requests, and aiofiles for the file-appends. These are two primary examples of IO that are well-suited for the async IO model.)

```python
# #!/usr/bin/env python3
# # areq.py
#
# """Asynchronously get links embedded in multiple pages' HMTL."""
#
import asyncio
import logging
import re
import sys
from typing import IO
import urllib.error
import urllib.parse

import aiofiles
import aiohttp
from aiohttp import ClientSession

logging.basicConfig(
    format="%(asctime)s %(levelname)s:%(name)s: %(message)s",
    level=logging.DEBUG,
    datefmt="%H:%M:%S",
    stream=sys.stderr,
)
logger = logging.getLogger("areq")
logging.getLogger("chardet.charsetprober").disabled = True

HREF_RE = re.compile(
    r'href="(.*?)"')  # HREF_RE is a regular expression to extract what we’re ultimately searching for, href tags within HTML:


async def fetch_html(url: str, session: ClientSession, **kwargs) -> str:
    """GET request wrapper to fetch page HTML.

    kwargs are passed to `session.request()`.
    """

    resp = await session.request(method="GET", url=url, **kwargs)
    resp.raise_for_status()  # Raises HTTPError, if one occurred.
    logger.info("Got response [%s] for URL: %s", resp.status, url)
    html = await resp.text()
    return html


async def parse(url: str, session: ClientSession, **kwargs) -> set:
    """Find HREFs in the HTML of `url`."""

    found = set()
    try:
        html = await fetch_html(url=url, session=session, **kwargs)
    except (
            aiohttp.ClientError,
            aiohttp.http_exceptions.HttpProcessingError,
    ) as e:
        logger.error(
            "aiohttp exception for %s [%s]: %s",
            url,
            getattr(e, "status", None),
            getattr(e, "message", None),
        )
        return found
    except Exception as e:
        logger.exception(
            "Non-aiohttp exception occured:  %s", getattr(e, "__dict__", {})
        )
        return found
    else:
        for link in HREF_RE.findall(html):
            try:
                abslink = urllib.parse.urljoin(url, link) # 절대 경로 url 생성
            except (urllib.error.URLError, ValueError):
                logger.exception("Error parsing URL: %s", link)
                pass
            else:
                found.add(abslink)
        logger.info("Found %d links for %s", len(found), url)
        return found


async def write_one(file: IO, url: str, **kwargs) -> None:
    """Write the found HREFs from `url` to `file`."""
    # 만약 parse()를 좀 더 세밀한 process로 관리하고 싶다면, 자체적으로 process를 생성하거나 threadPool를 생성한뒤
    # loop.run_in_executor()를 사용하는 것을 생각해 보아야 한다.
    # 여기서는 pool을 생성한 뒤, await loop.run_in_executor(pool, parse, url, **kwargs) 처럼 사용가능
    res = await parse(url=url, **kwargs)

    if not res:
        return None
    async with aiofiles.open(file, "a") as f:
        for p in res:
            await f.write(f"{url}\t{p}\n")
        logger.info("Wrote results for source URL: %s", url)


async def bulk_crawl_and_write(file: IO, urls: set, **kwargs) -> None:
    #     """Crawl & write concurrently to `file` for multiple `urls`."""
    async with ClientSession() as session:
        tasks = []
        for url in urls:
            tasks.append(
                write_one(file=file, url=url, session=session, **kwargs)
            )
        await asyncio.gather(*tasks)


if __name__ == "__main__":
    import pathlib
    import sys

    assert sys.version_info >= (3, 7), "Script requires Python 3.7+."
    here = pathlib.Path(__file__).parent

    with open(here.joinpath("urls.txt")) as infile:
        urls = set(map(str.strip, infile))  # url들의 순서 보장 x

    outpath = here.joinpath("foundurls.txt")
    with open(outpath, "w") as outfile:
        outfile.write("source_url\tparsed_url\n")

    asyncio.run(bulk_crawl_and_write(file=outpath, urls=urls))
```
- urls.txt에서 url을 읽어와 링크로 이동하여 GET req를 보낸뒤, resp를 받으면 이에 대한 regex(href)를 검사하고 이를 async with을 통해 foundurl.txt에 작성하는 소스코드이다. 

- It uses a single session, and a task is created for each URL that is ultimately read from urls.txt.

```
$ python areq.py
16:04:02 DEBUG:asyncio: Using selector: EpollSelector
16:04:02 INFO:areq: Got response [200] for URL: https://1.1.1.1/
16:04:02 INFO:areq: Found 15 links for https://1.1.1.1/
16:04:02 INFO:areq: Wrote results for source URL: https://1.1.1.1/
16:04:02 INFO:areq: Got response [200] for URL: https://www.github.com
16:04:02 INFO:areq: Found 97 links for https://www.github.com
16:04:02 INFO:areq: Wrote results for source URL: https://www.github.com
16:04:02 INFO:areq: Got response [200] for URL: https://naver.com/
16:04:02 INFO:areq: Found 176 links for https://naver.com/
16:04:02 INFO:areq: Wrote results for source URL: https://naver.com/
16:04:03 ERROR:areq: aiohttp exception for https://docs.python.org/3/this-url-will-404.html [404]: Not Found
16:04:03 INFO:areq: Got response [200] for URL: https://www.ietf.org/rfc/rfc2616.txt
16:04:03 INFO:areq: Found 0 links for https://www.ietf.org/rfc/rfc2616.txt
16:04:03 INFO:areq: Got response [200] for URL: https://www.bloomberg.com/markets/economics
16:04:03 INFO:areq: Found 3 links for https://www.bloomberg.com/markets/economics
16:04:03 INFO:areq: Wrote results for source URL: https://www.bloomberg.com/markets/economics
16:04:04 INFO:areq: Got response [200] for URL: https://www.politico.com/tipsheets/morning-money
16:04:04 INFO:areq: Found 149 links for https://www.politico.com/tipsheets/morning-money
16:04:04 INFO:areq: Wrote results for source URL: https://www.politico.com/tipsheets/morning-money
16:04:04 INFO:areq: Got response [200] for URL: https://www.nytimes.com/guides/
16:04:04 INFO:areq: Found 56 links for https://www.nytimes.com/guides/
16:04:04 INFO:areq: Wrote results for source URL: https://www.nytimes.com/guides/

$ wc -l foundurls.txt
    512 foundurls.txt

$ head -n 3 foundurls.txt
source_url	parsed_url
https://1.1.1.1/	https://www.cloudflare.com/careers/departments/
https://1.1.1.1/	https://1.1.1.1/#subscription-form
```

코드에서 몇가지 참고해야 하는 추가적인 포인트는

1. The default ClientSession has an adapter with a maximum of 100 open connections. To change that, pass an instance of asyncio.connector.TCPConnector to ClientSession. You can also specify limits on a per-host basis.

2. You can specify max timeouts for both the session as a whole and for individual requests.

3. This script also uses async with, which works with an asynchronous context manager. I haven’t devoted a whole section to this concept because the transition from synchronous to asynchronous context managers is fairly straightforward. The latter has to define .__aenter__() and .__aexit__() rather than .__exit__() and .__enter__(). As you might expect, async with can only be used inside a coroutine function declared with async def. 


실력을 더욱 기르고 싶다면 [aio-redis](https://github.com/aio-libs/aioredis)를 사용해서 URLs를 track하여 recursive 하게 crawl하도록 하라.

- avoid requesting them twice
- connect links with Python’s networkx library

Remember to be nice. Sending 1000 concurrent requests to a small, unsuspecting website is bad, bad, bad. There are ways to limit how many concurrent requests you’re making in one batch, such as in using the sempahore objects of asyncio or using a pattern like this one. If you don’t heed this warning, you may get a massive batch of TimeoutError exceptions and only end up hurting your own program.

- [semaphore](https://stackoverflow.com/questions/40836800/python-asyncio-semaphore-in-async-await-function)
- [concurrency with pattern](https://www.artificialworlds.net/blog/2017/05/31/python-3-large-numbers-of-tasks-with-limited-concurrency/)


## Async IO in Context
> Async IO를 사용해야 하는 상황들에 대하여

[Thinking Outside the GIL with AsyncIO and Multiprocessing - PyCon 2018](https://www.youtube.com/watch?v=0kXaLh8Fz3k&feature=youtu.be&t=10m30s)

Async IO는 다음과 같은 상황에서 option이 될 수 있다.

- Multiple, fairly uniform CPU-bound tasks (a great example is a grid search in libraries such as scikit-learn or keras)
    - grid search: 딥러닝에서 최적의 하이퍼 파라미터 조합을 검색하기 위해서 여러 파라미터값들을 조합해 가며 성능 테스트를 하는 것
- Multiprocessing should be an obvious choice.
- 많은 컴퓨터에서 수천 개의 스레드를 만들면 실패하므로 처음에는 시도하지 않는 것이 좋습니다. 수천 개의 비동기 IO 작업을 만드는 것은 완전히 가능합니다.
- IO bound 작업들
    - Network IO, whether your program is the server or the client side
    - Serverless designs, such as a peer-to-peer, multi-user network like a group chatroom
    - Read/write operations where you want to mimic a “fire-and-forget” style but worry less about holding a lock on whatever you’re reading and writing to
    



## async / await을 지원하는 라이브러리들
> Libraries That Work With async/await

From aio-libs:

- aiohttp: Asynchronous HTTP client/server framework
- aioredis: Async IO Redis support
- aiopg: Async IO PostgreSQL support
- aiomcache: Async IO memcached client
- aiokafka: Async IO Kafka client
- aiozmq: Async IO ZeroMQ support
- aiojobs: Jobs scheduler for managing background tasks
- async_lru: Simple LRU cache for async IO

From magicstack:

- uvloop: Ultra fast async IO event loop
- asyncpg: (Also very fast) async IO PostgreSQL support

From other hosts:

- trio: Friendlier asyncio intended to showcase a radically simpler design
- aiofiles: Async file IO
- asks: Async requests-like http library
- asyncio-redis: Async IO Redis support
- aioprocessing: Integrates multiprocessing module with asyncio
- umongo: Async IO MongoDB client
- unsync: Unsynchronize asyncio
- aiostream: Like itertools, but async