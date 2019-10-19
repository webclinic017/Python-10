# 2차원 정사각형배열에서 대각선 좌표 뽑아내는 helper

- `N`: 한변의 길이
- `start`: 시작 좌표들을 저장한 list
- `result`: 대각선 좌표를 저장하는 2차원 배열

```
1. start좌표를 생성한다.
2. 시작좌표에서 outofbound이전까지 while을 돌면서 result를 저장한다.
```

### 오른쪽 아래 대각선
```python
def right_down_diagonal(N=10):
    start = [(0, 0),]
    for y in range(1,N):
        start.extend([(0,y),(y,0)])
    result = [[] for _ in range(len(start))]
    for i,s in enumerate(start):
        ny,nx = s
        while ny<N and nx<N:
            result[i].append((ny, nx))
            ny += 1
            nx += 1
    return result
```
### 오른쪽 위 대각선
```python
def right_up_diagonal(N=10):
    start = [(N-1,0),]
    for y in range(1,N):
        start.extend([(y-1,0),(N-1,y)])
    result = [[] for _ in range(len(start))]
    for i,s in enumerate(start):
        ny,nx = s
        while ny>=0 and nx<N:
            result[i].append((ny, nx))
            ny -= 1
            nx += 1
    return result
```
