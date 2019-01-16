# ecoServer와 다르게 데이터를 여러 차례 송수신 할수있도록해보자.
import socket

def runServer(port=5050):
    host,bufsize = '',1024
    with socket.socket() as s:
        s.bind((host,port))
        s.listen(1)
        conn,addr=s.accept()
        while True:
            msg = conn.recv(bufsize)
            # 이렇게 보다 eof가 낫지 않을까?
            # 이렇게 하면 msg를 쓰지 않을경우라는 건데, 언제 buf가 비워졌다고 판단하는거지? 기준이 시간일까?
            # > client를 확인해보니, 빈문자열을 보낼경우 server에서 break먹도록 함.
            if not msg: break
            print(msg.decode())
            conn.sendall(msg)
        conn.close()

if __name__ == '__main__':
    runServer()