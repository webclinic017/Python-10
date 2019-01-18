# Greenlets

> gevent에서 사용되는 주된 패턴, C 모듈로 제공되는 경량 `coroutine`

- `Greenlets`들은 메인 프로그램을 실행하는 `OS process`안에서 모두 실행되지만 상호작용하며 스케쥴링 된다.
- 병렬로 실행되는 `multiprocessing`이나 `threading`을 이용한 병렬처리들과 다르게, 한번에 오직 하나의 `greenlet`만이 실행된다.


# Sync & Async
- Concurrence의 핵심 개념은 큰 단위의 task를 한번에 Sync하게 처리하는 대신, 작은 단위의 `subtask`들로 쪼개서 `async`하게 실행하는 것.
- 두 `subtask`간의 스위칭을 `context-switching` 이라한다.
- @ 여기서 subtask들은 thread들을 말하는 것일까? 아니면 single thread 하위에 subtask들이 있는 것일까? 만약 전자라면 thread들과 greenlet의 차이점은 사용자가 원하는 시점에 context-switching을 할 수 있다는 것이고, 후자라면 greenlet은 thread가 되고 spawn을 통하여서 subtask들을 생산하는 것이다.[thread vs greenlets](https://stackoverflow.com/questions/46528360/why-gevent-needs-synchronization-since-it-is-in-a-single-threaded)

[single thread기반으로 subtasks이 생성되는 것이다.](https://stackoverflow.com/questions/15556718/greenlet-vs-threads)

