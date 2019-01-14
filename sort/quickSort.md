
![](http://interactivepython.org/courselib/static/pythonds/_images/firstsplit.png)

![](http://interactivepython.org/courselib/static/pythonds/_images/partitionA.png)

![](http://interactivepython.org/courselib/static/pythonds/_images/partitionB.png)


# 코드
```python
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

```


# 결과

alist = [-2,-1,54,26,93,17,77,31,44,55,20]
2.151012420654297e-05
4.053354263305664e-05

alist=list(range(0,100))
0.0006070566177368164
0.0004073953628540039

alist = list(range(0,1000))
0.044204156398773196
0.002260761260986328


alist = list(range(0,100))
random.shuffle(alist)
0.00027112722396850587
0.00039268016815185546

alist = list(range(0,1000))
random.shuffle(alist)
0.0025422024726867677
0.003378286361694336




alist=list(range(0,1000)[::-1])
piv not random	0.04046363830566406
piv random	0.0023505401611328123


alist=list(range(0,2000))
piv not random	0.16436435222625734
piv random	0.005014631748199463
