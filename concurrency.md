[출처](http://atin.tistory.com/567)

# Concurrency(동시성)
- 논리적인 용어
- 동시에 실행되는 것처럼 보이는 것
- 싱글 코어에서 멀티 스레드를 동작시키기 위한 방식
    - 하지만 멀티 코어에서도 동시성은 사용 가능함
    - 코어 수에 따른 방식보다는 작업 방식에 대한 부분인데 굳이 이해하기 좋고 좁게 보자면 이렇게 이해할 수 있을꺼 같음
- 멀티 태스킹을 위해 여러 개의 스레드가 번갈아가면서 실행되는 성질
- 동시성을 이용한 싱글 코어의 멀티 태스킹은 각 스레드들이 병렬적으로 실행되는 것처럼 보이지만 사실은 번갈아가면서 조금씩 실행되고 있는 것

## 동시성 모델들
### 생산자 - 소비자(Produce-Consumer)
한 개 이상의 생산자가 생산한 작업물을 버퍼 혹은 큐에 넣는다. 한 개 이상의 소비자가 버퍼 혹은 큐에서 작업물을 습득, 작업을 마친다. 생산자와 소비자 사이에 있는 큐는 bound resource이다. 따라서 생산자는 큐에 남는 공간이 생길 때까지, 소비자는 큐에 작업물이 하나라도 생길 때까지 기다려야 한다. 큐를 통한 생산자와 소비자간의 조율에는 둘 사이의 시그널링이 필요하다. 생산자는 큐에 작업물을 넣고 소비자에게 “큐가 비어있지 않다”는 신호를 보내고 소비자는 큐에서 작업물을 꺼낸 후 “큐가 가득차 있지 않다”는 신호를 보낸다. 그 전까지 둘은 신호를 기다린다.

### 읽기-쓰기(Readers-Writers)
일반적으로 독자를 위한 정보로 사용되며, 가끔 저자에 의해 업데이트되는 공유 자원의 경우 처리량이 문제가 된다. 처리량을 강조해 독자가 상대적인 우선권을 가지게 되면 저자는 기아 상태에 빠지며 공유 자원은 정체된 정보로 가득차게 된다. 반대로 저자가 우선권을 가지면 처리량이 줄어들게 된다. 저자-독자 문제는 이 둘 사이의 균형을 맞추며 concurrent 업데이트를 방지하는 것을 주안점으로 둔다.

### 식사하는 철학자들(Dining Philosophers)
원탁을 둘러싼 여러 명의 철학자들이 있다. 각 철학자의 왼쪽에 포크가 놓여 있으며 테이블의 중앙에 큰 스파게티 한 그릇이 놓여 있다. 그들은 배가 고파지기 전까지 각자 생각을 하며 시간을 보낸다. 배가 고파지면 그들은 자신의 양쪽에 놓여 있는 포크 2개를 잡고 스파게티를 먹는다. 철학자는 포크 2개가 있어야만 스파게티를 먹을 수 있다. 그렇지 않다면 옆 사람이 포크를 다 사용하기 전까지 기다려야 한다. 스파게티를 먹은 철학자는 다시 배가 고파질 때까지 포크를 놓고 있게 된다. 위 상황에서 철학자를 스레드로, 포크를 공유 자원으로 바꾸게 되면 이는 자원을 놓고 경쟁하는 프로세스와 비슷한 상황이 된다. 잘 설계되지 않은 시스템은 deadlock, livelock, 처리량 문제, 효율성 저하 문제에 맞닥뜨리기 쉽다. 당신이 맞닥뜨릴 대부분의 concurrent관련 문제들은 이 세 가지 문제의 변형일 가능성이 높다. 이 알고리즘들을 공부하고 스스로 해법을 작성함으로써 이와 같은 문제들을 직면하더라도 의연하게 대처할 수 있도록 하자.



# Parallelism(병렬성)

- 물리적인 용어
- 실제로 작업이 동시에 처리되는 것
- 멀티 코어에서 멀티 스레드를 동작시키는 방식
- 한 개 이상의 스레드를 포함하는 각 코어들이 동시에 실행되는 성질
- 병렬성은 데이터 병렬성(Data parallelism)과 작업 병렬성(Task parallelism)으로 구분

## 병렬성 종류
    - 데이터 병렬성

        - 같은 작업을 병렬 처리하는 것
        - 전체 데이터를 나누어 서브 데이터들로 만든 뒤, 서브 데이터들을 병렬 처리하여 작업을 빠르게 수행하는 것
        - 자바 8에서 지원하는 병렬 스트림이 데이터 병렬성을 구현한 것
        - 서브 데이터는 멀티 코어의 수만큼 쪼개어 각각의 데이터들을 분리된 스레드에서 병렬 처리함
 
    - 작업 병렬성

        - 서로 다른 작업을 병렬 처리하는 것
        - Example) 웹 서버 (각각의 브라우저에서 요청한 내용을 개별 스레드에서 병렬로 처리함)

<p align="center"><img src="https://images.techhive.com/images/idge/imported/article/jvw/1998/09/concurrency-100158287-orig.gif"></p>

<p align="center">

<table align="center">
<tbody><tr><td style="width: 143px; height: 24px; border-width: 1px; border-style: solid; border-color: rgb(204, 204, 204); background-color: rgb(234, 234, 234);"><p>&nbsp;</p></td>
<td style="width: 325px; height: 24px; border-bottom: 1px solid rgb(204, 204, 204); border-right: 1px solid rgb(204, 204, 204); border-top: 1px solid rgb(204, 204, 204); background-color: rgb(234, 234, 234);"><p>&nbsp;<b>동시성(Concurrency)</b></p></td>
<td style="width: 395px; height: 24px; border-bottom: 1px solid rgb(204, 204, 204); border-right: 1px solid rgb(204, 204, 204); border-top: 1px solid rgb(204, 204, 204); background-color: rgb(234, 234, 234);"><p>&nbsp;<b>병렬성(Parallelism)</b></p></td>
</tr>
<tr><td style="width: 143px; height: 24px; border-bottom: 1px solid rgb(204, 204, 204); border-right: 1px solid rgb(204, 204, 204); border-left: 1px solid rgb(204, 204, 204);"><p>&nbsp;용어 차이</p></td>
<td style="width: 325px; height: 24px; border-bottom: 1px solid rgb(204, 204, 204); border-right: 1px solid rgb(204, 204, 204);"><p>&nbsp;논리적</p></td>
<td style="width: 395px; height: 24px; border-bottom: 1px solid rgb(204, 204, 204); border-right: 1px solid rgb(204, 204, 204);"><p>&nbsp;물리적</p></td>
</tr>
<tr><td style="width: 143px; height: 24px; border-bottom: 1px solid rgb(204, 204, 204); border-right: 1px solid rgb(204, 204, 204); border-left: 1px solid rgb(204, 204, 204);"><p>&nbsp;뜻</p></td>
<td style="width: 325px; height: 24px; border-bottom: 1px solid rgb(204, 204, 204); border-right: 1px solid rgb(204, 204, 204);"><p>&nbsp;동시에 실행되는 것처럼 보이는 것</p></td>
<td style="width: 395px; height: 24px; border-bottom: 1px solid rgb(204, 204, 204); border-right: 1px solid rgb(204, 204, 204);"><p>&nbsp;실제로 작업이 동시에 처리되는 것</p></td>
</tr>
<tr><td style="width: 143px; height: 24px; border-bottom: 1px solid rgb(204, 204, 204); border-right: 1px solid rgb(204, 204, 204); border-left: 1px solid rgb(204, 204, 204);"><p>&nbsp;코어 환경</p></td>
<td style="width: 325px; height: 24px; border-bottom: 1px solid rgb(204, 204, 204); border-right: 1px solid rgb(204, 204, 204);"><p>&nbsp;싱글&nbsp;코어, 멀티 코어에서 가능</p></td>
<td style="width: 395px; height: 24px; border-bottom: 1px solid rgb(204, 204, 204); border-right: 1px solid rgb(204, 204, 204);"><p>&nbsp;멀티 코어에서만 가능</p></td>
</tr>
</tbody></table>
<p></p>
