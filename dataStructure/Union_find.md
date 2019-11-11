# Union find
> disjoint set

- [`참조 소스코드`](https://brownbears.tistory.com/460)
- [`파이썬 자료구조 Disjoint set`](https://dongchans.github.io/2019/42/)
- [boj 문제1](http://blog.naver.com/kks227/220791837179)
- [boj 문제2](https://www.acmicpc.net/workbook/view/900)

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

- `by size`
```python
class Disjoint_set:
    def __init__(self,n):
        # segment size를 포함하는 list
        # 음수를 가진 녀석이 root, 나머지는 root의 idx를 가리키는 leaf
        self.data = [-1]*n
        self.size = n

    def find(self,idx):
        val = self.data[idx]
        return idx if val< 0 else val

    def union(self,a,b):
        print((a,b),self.data)
        a,b = map(self.find,(a,b))
        if a == b: return None

        if self.data[a] < self.data[b]:
            self.data[a] += self.data[b]
            self.data[b] = a
        else:
            self.data[b] += self.data[a]
            self.data[a] = b

        self.size -= 1



disjoint = Disjoint_set(10)
for a,b in zip(range(9),range(1,10)):
    if a in (3,7):continue
    disjoint.union(a,b)

disjoint.union(1,5)
disjoint.union(5,9)
print(disjoint.data)
```