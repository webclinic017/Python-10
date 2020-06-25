# Awaitable
> Task / Future / Coroutine
> [참고 자료](https://soooprmx.com/archives/6882)

## Future / Task의 의미

동기적으로 동작하는 코드에서는 `a = sync_do_something()`일 경우, return값을 blocking되어 반환 받는 것을 보증한다.
이와 달리 비동기적인 상황에서 `a = async_do_something()`는 a라는 변수에 결과값이 들어가 있다는 것을 보증하지 못한다.
그렇기 때문에 `Future`타입의 객체가 존재하게 되었으며(Task는 Future의 child 클래스), 이는 쉽게 말하면 미래에 값을 보증해줄것을 약속해준다. 
다시 말해서 리턴값을 기다리기 위해 blocking되는 시점을 미래로 옮겨주었다고 할 수 있다. (자바스크립트의 Promise, 또한 정확하게 설명하면 IO_Bound 작업의 경우에는 백그라운드로 동작하는 Event loop에 의해서 사용자 레벨의 Thread에서는 Blocking이 일어나지 않고,
단지 Kernel Thread를 통해 os에게 Blocking 되는 작업을 요청하고, os interrupt되는 시점에 결과값을 Event-loop를 통해서 전달받는다. (Selector), 코루틴을 여러개 만들어서 Blocking 되는 맥락을 현재 Main Thread에서 동작시키더라도 앞서 설명한 방식과 내부적인 동작 원리는 비슷하다. 
이 경우 `await IO_요청()`을 코루틴들을 loop하며 신청하게 되고 Blocking을 받게 되지만, 내부적으로 OS에게 IO task를 위임한다.)


## 스케쥴링 하기 ( = Task 생성하기 )
> Event-loop에 Schedule하는 방법 

Native Coroutine은 스케쥴러에 예약하여 실행한다. 즉 직접적으로 호출을 해서는 실행이 되지 않고 단지 coroutine object만 return 될 뿐이다.
이런 Native Coroutine을 실행하는 방법에 대해서 소개하겠다.

- `asyncio.ensure_future(coro) -> Task`
    - 코루틴 객체를 받아 Task를 return한다.
    - Task는 Event-loop가 작업하는 기본 단위로써, 코루틴을 wrap하고 있으며, Future를 상속받은 하위 클래스이다.
    - `concurrent.futures`의 `Executor.submit()`과 level만 다르고 거의 동일한 역할을 한다고 할 수 있다. 

- `asyncio.create_task()`
    - python 3.7부터 사용됨
    - `asyncio.ensure_future()`의 대체재
     




## 실행하기

- `for f in asyncio.as_completed(aws, *, loop=None, timeout=None)`
    - awaitable objects in the aws set들을 한번에 실행한다.
    - 이때 가장 먼저 result가 생성된 object부터 loop에서 값이 나오게 된다.
    - python 3.7이상 부터는 스케쥴 되지 않았다면 자동으로 스케쥴링 시켜준다. 

```python
# Python 3.7+
import asyncio
import random

async def lazy_greet(msg, delay=1):
    print(f'{msg!r} will be displayed in {delay} seconds.')
    await asyncio.sleep(delay)
    return msg.upper()

async def main():
    messages = 'hello world apple banana cherry'.split()
    cos = [lazy_greet(m, random.randrange(1, 5)) for m in messages]
    for f in asyncio.as_completed(cos):
        result = await f
        print(result)

asyncio.run(main())
```


- `asyncio.gather(*aws, loop=None, return_exceptions=False)`
    - aws 시퀀스에 있는 `awaitable objects`를 실행한다.
    - 어웨이터블이 코루틴이면 자동으로 태스크로 예약된다.
    - 반드시 코 루틴을 순서대로 실행하지는 않지만 입력과 동일한 순서로 결과 목록을 반환합니다.
    - list 타입으로 주어져야 하기 때문에, 메모리를 초과할 정도로 너무 리스트가 큰 경우에는 적합하지 않다.

```python
import asyncio
import random

async def lazy_greet(msg, delay=1):
    print(f'{msg!r} will be displayed in {delay} seconds.')
    await asyncio.sleep(delay)
    return msg.upper()

async def main():
    messages = 'hello world apple banana cherry'.split()
    cos = [lazy_greet(m, random.randrange(1, 5)) for m in messages]
    res = await asyncio.gather(*cos)
    print(res)

asyncio.run(main())
```
