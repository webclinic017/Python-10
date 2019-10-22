# N을 만드는 모든 자연수 조합


- `cache`를 활용하는 방법
```python
from itertools import product
_dict = dict()
def nums(i):
    if _dict.get(i,-1)!=-1: return _dict[i]
    _dict[i]= set()
    _dict[i].add((i,))
    if i != 1:
        for j in range(1,i):
            for a,b in product(nums(j),nums(i-j)):
                _dict[i].add(a+b)
    return _dict[i]
nums(4)
print(_dict)
```

- 조합을 활용하는 방법/ 위의 방법보다 비효율적
```python
result = []
def combination(N,comb=[]):
    global result
    leftover = N-sum(comb)
    if leftover == 0:
        result.append(comb)
        return
    s = 1 if comb == [] else comb[-1]
    for i in range(s,leftover+1):
        combination(N,comb+[i])
```