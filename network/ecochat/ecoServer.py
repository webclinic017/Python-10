# bind -listen - accept- read/write(turn)
import socket

def runServer(port=5050):
    # ip address
    # @host가 뭘까?
    host,bufsize = '',1024
    # with을 통하여 socket을 닫아준다.
    with socket.socket() as s:
        s.bind((host,port))
        # .listen(n): 원하는 클라이언트가 대기할 수 있는 큐의 크기
        s.listen(1)
        #  연결 요청을 수락한다.
        #  return 은 (client socket object,address)
        conn,addr = s.accept()
        # recv: 데이터를 읽을때 사용,
        msg = conn.recv(bufsize)
        # @f'{}'의미
        # msg는 byte로 들어오기 때문에 decode를 해준다.
        # @ decode()리턴은 string일듯
        print(f'{msg.decode()}')

        # 에코 방식으로 write 해준다.
        conn.sendall(msg)
        # 전달받은 socket object를 닫아준다. 
        conn.close()

if __name__ == '__main__':
    runServer()
