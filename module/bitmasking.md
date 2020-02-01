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

## `nCk` with bit operation

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
