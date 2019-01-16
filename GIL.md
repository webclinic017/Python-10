[출처](https://www.slideshare.net/deview/2d4python?ref=https://118k.tistory.com/606)

[출처2](https://steemit.com/kr-dev/@ethanhur/python-gil-python-concurrency)

# GIL(global Interpreter Lock)

> GIL 이란 파이썬에서 한번에 하나의 스레드만 수행할 수 있도록, 인터프리터에 `Lock`을 거는것이다.

- 결과적으로 스레드를 이용하여 프로그램을 구현하여 동시에 여러작업을 진행하여도, 한번에 하나의 작업만 돌게 되어 실제로는 작업시간이 더 늘어나는 결과를 가져온다.
- GIL에 의해 멀티스레딩 효율을 보지 못하기 때문에, Multiprocessing 모듈을 이용하면 된다.

## Implicit Scheduling
>  어떤 thread로 넘어갈지는 사실상 랜덤

python은 별도의 thread 스케쥴링 없이, 시스템이 제공하는 threading lib의 lock mechanism에 의해 context switch가 발생

## GIL 사용 이유

1. single thread 성능에 우위

    - Python은 mem 관리를 `reference counting` 방법으로 한다. GIL에 대비되는 fine-grained lock 방법을 사용할 경우 모든 객체의 접근마다 lock으로 관리해야 하므로 그 overhead가 매우 크다.
    
    - I/O bound
        - 한 프로그램이 I/O를 많이 쓰면 대부분 I/O bound 이기 때문에 파이썬의 쓰레드를 사용하는 것이 좋은 경우도 있다.
        
        [부가설명](https://stackoverflow.com/questions/29270818/why-is-a-python-i-o-bound-task-not-blocked-by-the-gil)
        - 좀 더 부가 설명) 비동기 호출로 I/O가 걸리는 순간, GIL이 풀리면서 다른 Thread가 실행되게 된다. (@ 왜 강제 context swith가 발생할까? )
        - 따라서 I/O가 많은 프로그램에서는 GIL을 쓰는 단점을 그렇게 느끼지 못하고, 오히려 GIL의 경우에는 single thread의 성능이 우위에 있기에 장점이 더 부각 되는 느낌이다.



2. C 확장 개발에 용이
3. Garbage Collector 만들기 좋다.

## GIL 단점

  - `CPU bound(CPU intensive process)`의 경우에는 한 쓰레드에서 연산을 하는 동안 다른 쓰레드는 놀고 있기 때문에 GIL이 문제가 된다.
  
  
## CPU bound 해결법
  - C extension 사용
      - Lock의 범위 밖에 있으므로 연산을 위해 C extension으로 요청을 보내는 순간, 이를 I/O와 똑같이 판단하여 Lock을 푼다.
      - 물론 속도도 매우 빨라진다.
      
  - Multiprocess 사용
      - 쓰레드를 여러개 띄우는 것이 아닌, 프로세스를 여러개 띄우면 된다.
      - Process는 메모리 입장에서도 독립적인 단위이기에 `Lock`이 따로 걸려, process 마다 병렬 처리 가능하다.
## 결론 
    - 파이썬의 경우에는 Concurrent 프로그램을 구현할때 GIL을 염두에 두고 구현해야 한다. 아마도 `gevent`사용하면 해결 될듯.
