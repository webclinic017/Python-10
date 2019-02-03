# string match

## 1. Brute_forece

  - 1. base: T[0],P[0]부터 시작, t<len(T) 루프를 돌면서
  - 2. match check-> index move && if match completed check를 p가 len(p) 갈떄 while을 빠져나오도록 한다. 이후 if 문을 통하여 return값 계산
  - 3. when loop end, res = -1 or t
  - **`O(T*P)`**

```python
def bruteForce(T,P):
  # range는 마지막 녀석 포함 하지 않으니까 -1 없애준다.
  t=p=0
  while t<len(T) and p<len(P):
    if T[t]==P[p]: t+=1;p+=1;continue
    t=t-p+1;p=0
  print(t-len(P)) if p==len(P) else print(-1)

text = "TTTTTTCCTAA"
pattern = "AA"
bruteForce(text,pattern)
```

## 2. KMP

