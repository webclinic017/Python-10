# Event-loop

## loop 실행 방법

- `Asyncio.run()`
    - 3.7 이후 버전에서의 Event-loop를 돌리는 방법(Single Thread 기반)
    
- `loop.run_until_complete(future)`
    - block everything until we have a result (`run()`의 하위 버전)

- `loop.run_in_executor(executor, func, *args)`
    - 스레드 또는 프로세스 풀에서 코드를 실행하기

c.f) 참고로 python 3.8에서는 `python -m asyncio`를 사용하여 쉘을 시작하면 쉘 자체가 런루프 내에서 돌아가게 된다.
즉 비동기 코루틴 함수를 실행해서 코루틴을 바로 실행 가능하다.

