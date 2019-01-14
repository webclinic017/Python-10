# easy try
# 하지만 mergesort랑 다를것이 없다. 왜냐하면 left ,right로 extra array를 O(n) 만큼 생성하기 때문이다.

def quickSort(li):
    li_len = len(li)
    if li_len<=1:
        return li
    piv = li[0]
    left = [i for i in li[1:] if i<=piv]
    right = [i for i in li[1:] if i>piv]
    
    return quickSort(left)+[piv]+quickSort(right)


a = [1,2,3,4,5,6,7,8,9,500,400,300,200,100,99,59]
print(quickSort(a))


# second try
# without extra mem

import random
import time

def quickSort(li):
    quickHelper(li,0,len(li)-1)

def quickHelper(li,first,last):
    if first<last:
        split=partition(li,first,last)
        quickHelper(li,first,split-1)
        quickHelper(li,split+1,last)

def partition(li,first,last):
#     # random pivot part
#     inx = random.randint(first,last)
#     li[first],li[inx] = li[inx],li[first]

    piv_v,left,right = li[first],first+1,last
    flag = False

    while not flag:
        while left <=right and li[left]<=piv_v:
            left += 1
        while right >= left and li[right] >= piv_v:
            right -= 1
        if right < left: flag = True
        else:
            li[left],li[right] = li[right],li[left]
    li[first],li[right] = li[right],li[first]
    return right

start = time.time()
for i in range(100):
    alist = list(range(0,1000))
#     random.shuffle(alist)
    quickSort(alist)
    # print(alist)
print((time.time()-start)/100)
