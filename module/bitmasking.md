# 비트 마스킹
> https://sangdo913.tistory.com/7

## python binary print
- `PB = lambda n :'{:08b}'.format(n) #Print Binary`

## Binary One's Complement(`~a`)
> 모든 bit를 reverse 시키게 되며, 이는 -(x+1)-> -x-1 이 되는 결과
```python
a = 2
print(PB(~a)) # -3, -0000 0011
```
## Binary Two's Complement(`-a`)
> 모든 bit를 reverse +1 시키게 되며, 이는 -x-1+1 -> -x 이 되는 결과
```python
a = 2
print(PB(-a)) # -2, -0000 0010
```

```
a = 1000 1000
-a = 0111 1000
```
- 가장 오른쪽에 존재하는 1을 기준으로 왼쪽은 One's complement(just reverse), 오른쪽은 0으로 존재


## 최하위 비트 구하기

- `a & -a` : 최하위 비트 1을 제외하고는 0으로 변한다.
```python
a = 2 # 0000 0010
b = -a # 1111 1110
a&b = # 0000 0010
```
- `~a &  -~a`==`~a&(a+1)`: 최하위 비트 0을 제외하고는 0으로 변한다.

```
a   =   1010 0110
~a  =   0101 1001
-a  =   0101 1010
~~a=a=  1010 0110
-~a =   1010 0111
~a&-~a= 0000 0001
```

## 멱집합(powerset, 부분집합)
> https://blog.naver.com/PostView.nhn?blogId=kmh03214&logNo=221702095617
```python
def powerset(s):
    masks = [1<<i for i in range(len(s))]
    for i in range(1<<len(s)):
        yield [ss for ss,mask in zip(s,masks) if mask&i]
```

## `nCk` with bit operation

- stack overflow 소스코드(이해하기 어렵)
```python
# 모든 combination
def bitmasks(n,m):
    if m < n:
        if m > 0:
            for x in bitmasks(n-1,m-1):
                yield (1 << (n-1)) + x
            for x in bitmasks(n-1,m):
                yield x
        else:
            yield 0
    else:
        yield (1 << n) - 1
```

- 내가 만들어본 비트마스킹을 활용한 조합 코드
```python
def combination(n,m):
    for i in range(1<<n):
        comb = []
        _bin = '{:0{}b}'.format(i,n)
        for j,b in enumerate(_bin):
            if b=='0':continue
            if len(comb)>m:break
            comb.append(j)
        else:
            if len(comb)==m: yield comb
            
arr = [1,2,3,4,5]
for p in [comb for comb in combination(len(arr),3)][::-1]:
    print([arr[pp] for pp in p])
```
- 순서를 보장.
- 파이썬이 str(->bin())을 사용해야만 bit masking을 사용할 수 있는 것 같다.
