# 쓰레드를 활용하여 listen파트(main thread)와 send파트(sub thread)를 나누어야 한다.

# @ 파이썬에서 쓰레드 쓰지 말라고 했는데, 왜 그럴까
# @ 만약 쓰지 않는다면 어떤 방식을 사용할 수 있을까? 
from threading import Thread
import socket,time,random

def broadcast(sock,words):
    bufsize=1024
    while True:
        # msg = sock.recv(bufsize)
        # if not msg: break
        word = random.choice(words).strip()
        sock.sendall(word.encode())
        time.sleep(1)
    sock.close()

def readwords(path):
    words = 0
    with open(path,"r") as f:
        words = f.readlines()
    return words

def runServer(port=8000):
    host = ''
    words = readwords('./words.txt')
    with socket.socket() as s:
        s.bind((host,port))
        while True:
            print("대기중")
            s.listen(1)
            conn,_ = s.accept()
            print("접속됨")
            # @파이썬에서 (var,) ,콤마의 의미는 뭘까? 왜 이딴식으로 하지
            # eval에서도 이런식으로 했었는데. 
            Thread(target=broadcast,args=(conn,words)).start()
            
if __name__=='__main__':
    runServer()