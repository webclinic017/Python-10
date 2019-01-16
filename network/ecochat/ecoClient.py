# connect - write - read
import socket

def run():
    ip,port,bufsize = '127.0.0.1',5050,1024
    with socket.socket() as s:
        s.connect((ip,port))
        # encode 바이트화
        s.sendall(input(':').encode())
        resp = s.recv(bufsize)
        # @ f'>' 의미는?
        print(f'>{resp.decode()}')
if __name__ == '__main__':
    run()

