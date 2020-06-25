# loop.run_until_complete()
> 3.7 이상부터는 asyncio.run()을 사용해서 코드를 실행한다.

하위 버전과의 호완을 위해 run()을 재정의 하는 것을 택한다. 아래는 run()이 돌아가는 방식을 정의함과 동시에, 기본적으로 python `run()`이 어떤 원리로 돌아가는지 보여준다.

```python
def run(aw):
    if sys.version_info >= (3, 7):
        return asyncio.run(aw)

    # Emulate asyncio.run() on older versions
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        return loop.run_until_complete(aw)
    finally:
        loop.close()
        asyncio.set_event_loop(None)
```

