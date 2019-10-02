import socket,time
from threading import Thread

# word 클래스를 만들어서 string을 좌표가 있는 word 형식으로 생성
# score 생성해준다.
#  GUI 만들어준다.
def move():
    global word_queue
    while True:
        print(word_queue)
        time.sleep(2)
    
    
def run():
    global word_queue
    ip,port,bufsize = '127.0.0.1',8000,1024
    with socket.socket() as s:
        s.connect((ip,port))
        Thread(target=move).start()
        while True:
            # msg = input(':')
            # s.sendall(msg.encode())
            # if not msg:break
            word = s.recv(bufsize).decode()
            word_queue.append(word)
            # print()

if __name__ == '__main__':
    word_queue=[]
    run()