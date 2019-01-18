# import gevent
# from gevent.queue import Queue
# from gevent.server import StreamServer
# import random,string

# # 연결된 client에게 단어를 1초 단위로 쏴준다. 
# # 클라이언트의 연결이 끊어질때까지 단어를 쏴주면 끝
# wordfile = open('words.txt', 'r')
# word = wordfile.readline()

# users = {}  # mapping of username -> Queue

# HOST,PORT,SIZE = '',5050,1024

# def server_handler(connection, address):
#     print('new connection by', address)
#     data_stream = data_stream_gen()
#     while True:
#         chunk = str.join('', (next(data_stream) for i in range(SIZE)))
#         connection.sendall(chunk)
#         with open('server.txt', 'w') as log:
#             log.write(chunk)

# def data_stream_gen():
#     while True:
#         yield random.choice(string.ascii_lowercase)

import gevent
from gevent.queue import Queue
from gevent.server import StreamServer

users = {}  # mapping of username -> Queue


def broadcast(msg):
    msg += '\n'
    for v in users.values():
        v.put(msg)


def reader(username, f):
    for l in f:
        msg = '%s> %s' % (username, l.strip())
        broadcast(msg)


def writer(q, sock):
    while True:
        msg = q.get()
        sock.sendall(msg.encode())


def read_name(f, sock):
    while True:
        sock.sendall('Please enter your name: '.encode())
        name = f.readline().strip()
        if name:
            if name in users:
                sock.sendall('That username is already taken.\n'.encode())
            else:
                return name


def handle(sock, client_addr):
    f = sock.makefile()

    name = read_name(f, sock)

    broadcast('## %s joined from %s.' % (name, client_addr[0]))

    q = Queue()
    users[name] = q

    try:
        r = gevent.spawn(reader, name, f)
        w = gevent.spawn(writer, q, sock)
        gevent.joinall([r, w])
    finally:
        del(users[name])
        broadcast('## %s left the chat.' % name)


if __name__ == '__main__':
    import sys
    # try:
    #     myip = sys.argv[1]
    # except IndexError:
    #     myip = '0.0.0.0'
    myip = '127.0.0.1'

    print('To join, telnet %s 8001' % myip)
    s = StreamServer((myip, 8001), handle)
    s.serve_forever()




