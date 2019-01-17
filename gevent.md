# Greenlets

> gevent에서 사용되는 주된 패턴, C 모듈로 제공되는 경량 `coroutine`

- `Greenlets`들은 메인 프로그램을 실행하는 `OS process`안에서 모두 실행되지만 상호작용하며 스케쥴링 된다.
- 병렬로 실행되는 `multiprocessing`이나 `threading`을 이용한 병렬처리들과 다르게, 한번에 오직 하나의 `greenlet`만이 실행된다.


# Sync & Async
- Concurrence의 핵심 개념은 큰 단위의 task를 한번에 Sync하게 처리하는 대신, 작은 단위의 `subtask`들로 쪼개서 `async`하게 실행하는 것.
- 두 `subtask`간의 스위칭을 `context-switching`
