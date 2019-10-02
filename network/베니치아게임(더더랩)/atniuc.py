from threading import Thread
from collection import deque

n = 0
def tmp():
    global n
    for i in range(1,100000000):
        n +=1

if __name__=='__main__':
    Thread(target=tmp).start()
    Thread(target=tmp).start()
    print(n)
    
# java에서는 blocking queue
# 주의할점은 queue가 가득찰때 멈추므로 main도 멈춰버린다.
         23

greater = [item[1] for item in filter(lambda x: x[1] > x[0], zip(lst, lst[1:]))]
li = [3, 5, 2, 3, 1, 2, 3, 1, 3]
