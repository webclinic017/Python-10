import gevent
from gevent.event import Event

'''
Illustrates the use of events
'''

# evt = Event()
def setter():
    while True:
        setter2()
        gevent.sleep(2)
def setter2():
    print("Good morning")
    # listener
    # '''After 3 seconds, wake all threads waiting on the value of evt'''
    # # while 서버에 응답이 올때마다 list에 단어 저장

    # print('A: Hey wait for me, I have to do something')
    # gevent.sleep(1)
    # print("Ok, I'm done")
    # # evt.set()

def waiter():
    # move 
    # while 윈도우 창을 벗어나지 않으면서, 라이프가 0이 되지 않을때까지 move
    
    for i in range(1,10000):
        print(i)
        gevent.sleep(1)
    
    print("It's about time")

def main():
    gevent.joinall([
        gevent.spawn(setter),
        gevent.spawn(waiter)
    ])

if __name__ == '__main__': main()