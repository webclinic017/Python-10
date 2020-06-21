# Coroutine

파이썬에서 `Coroutine`이라는 용어는 다양하게 활용되었습니다. 과거의 `제너레이터의 특수한 형태`에서 현재
`asyncio`에서 사용되는 `Coroutine type`까지 파이썬의 버전에 따라 다양하게 모습을 변화하여 사용되었기 때문에 저 또한 공부하며 많은 혼란을 겪었습니다. 이번에는 `코루틴`이 사용되었던 도메인들에 대해서 과거와 현재(`3.8-dev`)를 비교하며 특성을 정리하겠습니다.

## generator
들어가기 앞서 generator에 대해서 짧게 알아보도록 하겠습니다. 제너레이터의 특징은 다음과 같습니다.

1. 제너레이터는 yield를 통하여 여러번 return을 할 수 있습니다.

2. 이때 yield를 통해 caller에게 값을 전달함과 동시에 권한 또한 양도합니다. 

3. 이 때 제너레이터 속안의 state(상태)는 권한이 양도되었더라도 함수(call stack pop때 state가 사라짐)와 달리, state가 유지됩니다.

## `generator 기반 coroutine` (3.3)
> 과거의 Coroutine

과거 python에서 coroutine이라는 용어는 `제너레이터의 특수한 형태`를 뜻하였습니다.
기존의 `generator`가 상태를 유지하며, 여러번 값을 yield할 수 있다면, `coroutine`은 `상호작용이 가능한 generator`의 의미로 사용되었습니다. 
즉 output 기능만 있던 제너레이터에 input을 받을 수 있는 제너레이터 타입이 `제너레이터 기반 코루틴`으로 명칭되어 사용되었습니다.
하지만 실제로 `코루틴`이라 명칭되어 사용되었던 코드(`yield (value)`, `yield from`을 내포하는 제너레이터)는 타입을 찍어보면, `<generator>` 타입으로 찍혀서 나타나는 것을 확인 할 수 있습니다. 


- `(yield)`
```python
def consumer_coro():
    while True:        # 코루틴을 계속 유지하기 위해 무한 루프 사용
        x = (yield)    # 코루틴 바깥에서 값을 받아옴, yield를 괄호로 묶어야 함
        print(x)
 
coro = consumer_coro()
next(coro)      # 코루틴 안의 yield까지 코드 실행(최초 실행)
print(type(coro)) # generator 

for i in range(5):
    coro.send(i) # producer
```

- `(yield from)`
```python
# 코루틴 1
def accumulate():
    total = 0
    while True:
        x = (yield)  # 코루틴 바깥에서 값을 받아옴
        if x == 'EXIT':  # 받아온 값이 EXIT이면
            raise StopIteration(total) # 3.6 이하 까지만, StopIteration를 yield from이 잡아낸다.
        total += x

# 코루틴 2
def sum_coroutine():
    while True:
        total = yield from accumulate()  # accumulate의 반환값을 가져옴
        print(total)


co = sum_coroutine()
next(co)

for i in range(1, 11):  # 1부터 10까지 반복
    co.send(i)  # 코루틴 accumulate에 숫자를 보냄
co.send('EXIT')  # 코루틴 accumulate에 EXIT을 보내서 숫자 누적을 끝냄

for i in range(11, 21):  
    co.send(i)  # 코루틴 accumulate에 숫자를 보냄
co.send('EXIT')  # 코루틴 accumulate에 EXIT을 보내서 숫자 누적을 끝냄
```

## `@asyncio.coroutine`의 코루틴 (3.4) 

**Coroutines use the `yield from` syntax introduced in PEP 380, instead of the original `yield` syntax.**

```python
@asyncio.coroutine
def coro():
    # 기능 1. 권한 양도하기
    변수 = yield from coroutine
    변수 = yield from future
    변수 = yield from task
    
    # 기능 2. 값 생산
    # 다른 coroutine에서 yield from coro()하고 있을 경우
    # produce a result to the coroutine that is waiting for this coro
    return expression # produce value
    raise exception # raise an exception
```

파이썬 3.3에서 asyncio는 pip install asyncio로 asyncio를 설치한 뒤 @asyncio.coroutine 데코레이터와 yield from을 사용하면 됩니다. 
단, 3.3 미만 버전에서는 asyncio를 지원하지 않습니다.

- `@asyncio.coroutine`
```python
import asyncio


@asyncio.coroutine
def accumulate(coro_name, n, m):
    print(f'{coro_name} is started!')
    total = n
    while total < m:
        print("SLEEP", coro_name)
        yield from asyncio.sleep(.1)
        total += 1
    return total


@asyncio.coroutine
def sum_coroutine(*args):
    total = yield from accumulate(*args)  # accumulate의 반환값을 가져옴
    print("result : ", total)
    return total


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    nums = [('coro1', 1, 11), ('coro2', 11, 21)]
    tasks = [asyncio.ensure_future(sum_coroutine(*args)) for args in nums]
    loop.run_until_complete(asyncio.wait(tasks))

```

- 결과값
```bash
coro1 is started!
SLEEP coro1
coro2 is started!
SLEEP coro2
SLEEP coro1
SLEEP coro2
SLEEP coro1
SLEEP coro2
SLEEP coro1
SLEEP coro2
SLEEP coro1
SLEEP coro2
SLEEP coro1
SLEEP coro2
SLEEP coro1
SLEEP coro2
SLEEP coro1
SLEEP coro2
SLEEP coro1
SLEEP coro2
SLEEP coro1
SLEEP coro2
result :  11
result :  21
```
- 위와 같이 @asyncio에서의 coroutine은 하나의 Thread에서 context switching을 원하는 시점에 할 수 있도록 만들어준다. 
- 대신 `3.3`에서 처럼 `x = (yield)`의 기능은 하지 못한다. (3.6 부터는 가능)

다음은 3.6버전에서 async for를 사용한 (yield) 기능 + `native async`을 동시에 구현한 모습이다.
```python
import asyncio


async def accumulate(coro, n, m):
    print(coro + "is started!")
    total = n

    while total < m:
        print(f'{coro} is yielding {total}')
        yield total
        total += 1
        print(f'{coro} is sleeping')
        await asyncio.sleep(.1)


async def sum_coroutine(*args):
    total = [i async for i in accumulate(*args)]  # accumulate의 반환값을 가져옴
    print("result : ", total)
    return total


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    nums = [('coro1', 1, 11), ('coro2', 11, 21)]
    tasks = [asyncio.ensure_future(sum_coroutine(*args)) for args in nums]
    loop.run_until_complete(asyncio.wait(tasks))
```

output
```bash
coro1is started!
coro1 is yielding 1
coro1 is sleeping
coro2is started!
coro2 is yielding 11
coro2 is sleeping
coro1 is yielding 2
coro1 is sleeping
coro2 is yielding 12
coro2 is sleeping
coro1 is yielding 3
coro1 is sleeping
coro2 is yielding 13
coro2 is sleeping
coro1 is yielding 4
coro1 is sleeping
coro2 is yielding 14
coro2 is sleeping
coro1 is yielding 5
coro1 is sleeping
coro2 is yielding 15
coro2 is sleeping
coro1 is yielding 6
coro1 is sleeping
coro2 is yielding 16
coro2 is sleeping
coro1 is yielding 7
coro1 is sleeping
coro2 is yielding 17
coro2 is sleeping
coro1 is yielding 8
coro1 is sleeping
coro2 is yielding 18
coro2 is sleeping
coro1 is yielding 9
coro1 is sleeping
coro2 is yielding 19
coro2 is sleeping
coro1 is yielding 10
coro1 is sleeping
coro2 is yielding 20
coro2 is sleeping
result :  [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
result :  [11, 12, 13, 14, 15, 16, 17, 18, 19, 20]
```


## `async def`의 코루틴 (3.5 ~)
> 네이티브 코루틴의 등장, 이전까지의 코루틴은 `제너레이터 코루틴`이라고 칭한다.

```python
import asyncio

async def nested():
    return 42

async def main():
    coro = nested() # 아무런 일도 일어나지 않는다.
    print(type(coro)) # <class 'coroutine'>
    result = await nested()  # 42
    print(result)

asyncio.run(main())
```

## async generator (3.6 ~)

- async, await in comprehension
- await, yield 동시 사용가능 in body

## `asyncio.run()` (3.7 ~ )


## 추가 읽어볼 거리

- [파이썬의 비동기 IO : 완전한 연습](https://realpython.com/async-io-python/)