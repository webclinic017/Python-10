dir()
String.startswith()
.split() : return list & ' '는 모두 같이 처리된다.


## collection (dict)

- `in`을 사용하여 dict key들에 해당 요소가 있는지 확인가능.
```python
ccc = {'a': 123,'b':345,'c':567 }

# return False
'd' in ccc

# return True
'a' in ccc
```
- list count to dict() 
- `get()`이라는 함수가 하는 역활
    - 키가 없다면 키를 생성하고 default 값을 넣어주는 역활
    - `cnt=dict(); [cnt.__setitem__(name,cnt.get(name,0)+1) for name in names]`

```python
names = ['a','a','a','b','b','c']
cnt=dict(); [cnt.__setitem__(name,cnt.get(name,0)+1) for name in names]
print(cnt)
# {'a': 3, 'b': 2, 'c': 1}
```
위와 똑같은 코드
```python
#names is list() sth
cnt = dict()
for i in names:
    if i not in cnt:
        cnt[i]=1
    else:
        cnt[i]+=1
```

- `.keys()`: return list()
- `.values()`: return list()
- `.items()`: return list(tuple(), tuple(), ....)


- 파일을 읽어와서 단어별 빈도수 세기 코드
```python
dic = dict()
[dic.__setitem__(word,dic.get(word,0)+1) for word in line.rstrip().split() for line in open(file)]
```
