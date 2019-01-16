import socket
def run():
    ip,port,bufsize = '127.0.0.1',8080,1024
    with socket.socket() as s:
        s.connect((ip,port))
        while True:
            msg = input(':')
            s.sendall(msg.encode())
            if not msg:break
            print(s.recv(bufsize).decode())

if __name__ == '__main__':
    run()

# >>> if '':
# ...     print(1)
# ...
# >>>
# >>> if not '':
# ...     print(1)
# ...
# 1
# >>> print(bool(''))
# False


    