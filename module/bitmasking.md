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
- `~a &  -~a`: 최하위 비트 0을 제외하고는 0으로 변한다.
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

def get_zeros(n):
    num = 0
    while ((n&1)==0):
        num+=1
        n >>=1
    return num

def func(bit,n):
    msb = 1 << (n-1)
    while(msb):
        print(bin(msb&bit))
        msb >>= 1

num = [0]*15
n,m = map(int,input().split())
for i in range(n):
    num[i] = int(input())

bit = (1<<m) -1
while (bit < (1<<n)):
    func(bit,n)
    temp = bit | ((bit & -bit) -1)
    bit = (temp+1) | (((~temp & -~temp) -1) >> (get_zeros(bit)+1))

```