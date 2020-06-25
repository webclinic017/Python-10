# async with ( async context manager )
> [sooooprmx](https://soooprmx.com/archives/8629)

파이썬에서 context manager는 `with` block을 적용할 수 있는 객체를 말합니다.
이런 객체를 만들기 위해서는 다음 2가지 magic method가 필요합니다

- `__enter__()` : 해당 블록에 들어올 때 적용 
- `__exit__()` : 해당 블록을 빠져나갈 때 적용


## async with

파이썬 3.5부터 비동기 컨텍스트 매니저가 도입되었습니다. 비동기적으로 IO 작업들에 대해서 리소스를 열고 닫고 할 때 사용가능합니다.
해당 비동기 컨텍스트 매니저는 앞서 소개되었던 magic method에 'a'를 붙이 다음의 2가지 method를 통해 정의합니다.

- `__aenter()__`
- `__aexit()__` 

주의해야할 점은 이 둘 모두 내부에서 `await`를 할 수 있는 awaitable이어야 하기 때문에, `async def`키워드를 통해
`비동기 코루틴`으로 작성되어야 합니다.

## Example

```python
'''
THis is a simple implementation about pyhton async context manager.

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
```
