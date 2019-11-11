# Union find
> == disjoint set

## 1. 배열을 사용하는 방식
```
O(N)
1. 먼저 원소의 크기만큼 배열을 초기화
2. 모든 원소 순회 하며, parent 교체
```
```python
class Disjoint_set:
    def __init__(self,n):
        self.data = list(range(n))
        self.size = n
        pass

    def union(self,a,b):
        a,b = map(self.find,[a,b])

        if a==b:return

        for i in range(self.size):
            if self.find(i)==b:
                self.data[i]=a

    def find(self,idx):
        return self.data[idx]

    @property
    def num_group(self):
        return len(set(self.data))

disjoint = Disjoint_set(10)
for a,b in zip(range(9),range(1,10)):
    if a in (3,7):continue
    disjoint.union(a,b)

print(disjoint.data)
print(disjoint.num_group)
```

## 2. Tree를 사용하는 방식
- union by size
- union by height
