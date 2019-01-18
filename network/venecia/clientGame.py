# 서버가 쏴주는 단어는 list에 append
#   1) receive part
#  서버의 전달을 계속 주시한다.
#  클라이언트가 종료될때, 또는 life가 0이 될때 close한다.

#   2) move part && show part
#   - 시간에 따라서 모든 단어들의 y축이 바뀐다.


#   - 단어를 받을 때 마다 화면에 쏴준다.
#   - x 값은 window.size()-word.length()에서 random
#   - 단어의 위치는 시간에 따라서 y축이 내려간다.

#   - score 맞은 단어의 갯수
#   - life 5개
#   - id: client를 시작할때 id를 쓰도록한다.

#   3) keyboard part
#  키보드의 입력을 계속 주시한다.

import socket
def run():
    ip,port,bufsize = '127.0.0.1',8001,1024
    with socket.socket() as s:
        s.connect((ip,port))
        while True:
            msg = input(':')
            s.sendall(msg.encode())
            if not msg:break
            print(s.recv(bufsize).decode())

if __name__ == '__main__':
    run()