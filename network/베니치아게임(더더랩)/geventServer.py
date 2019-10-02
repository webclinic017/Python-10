from __future__ import print_function
from gevent import sleep
from gevent.server import StreamServer
from gevent.pool import Pool
# what is StreamServer? vs socket
import time,random

def readwords(path):
    words = 0
    with open(path,"r") as f:
        words = f.readlines()
    return words

def broadcast(socket, addr):
    print('New connection from %s:%s' % addr)
    # socket.sendall(b'Welcome to the echo server! Type quit to exit.\r\n')
    while True:
        word = random.choice(words).strip()
        socket.sendall(word.encode())
        sleep(1)
    # while True:
    #  input이 주어지면 왜 socket이 막히는가 -> telnet에서만 발생하는 문제
    # sleep의 시간 이후에는 어떤 콜백함수가 작용되는가

        

if __name__=='__main__':
    # do not accept more than 5000 connections
    # 동시에 5000개 까지 연결 가능
    pool = Pool(5000)
    words = readwords('./words.txt')

    server = StreamServer(('127.0.0.1',8080),broadcast, spawn=pool)
    server.serve_forever()