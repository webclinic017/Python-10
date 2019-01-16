# 파이썬 서버 클라이언트 프로그래밍

- STL 사용
    - Multiprocessing
   
        - from threading import Thread
            - 기본적으로 파이썬의 [`GIL`(global interpreter lock)](https://github.com/minkj1992/Python/tree/master) 이슈 때문에 thread를 사용하는 것은 비추천 되고 있다.
          
        - from multiprocessing import Process
        - from multiprocessing import Pool
        - from Councurrent import futures
            - [링크](https://soooprmx.com/archives/5669)
        
    - Multiplexing
    
- gevent 사용
    - [듀랑고](https://www.slideshare.net/sublee/spof-mmorpg)
    - [듀랑고2](https://www.slideshare.net/sublee/lt-vol-2)
    - [듀랑고3](https://www.slideshare.net/sublee/vol-3-95472828)
    
- ZMQ 사용
    - [wireframe의 zmq](https://soooprmx.com/archives/6436)
    -
    
- c.f 
    - [파이썬 동시성](http://hamait.tistory.com/833)
    - [파이썬 Asyncio](http://hamait.tistory.com/834?category=79136)
    - [자바와 파이썬 연결](http://hrepository.blogspot.com/2017/04/python-java-socket.html)
