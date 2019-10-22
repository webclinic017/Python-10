# roate

# 1d rotate
## clock-wise
```python
def clock(arr,n):
    n%=len(arr)
    return arr[len(arr)-n:]+arr[:len(arr)-n]
```
## counter-clock-wise
```python
def counter_clock(arr,n):
    n%=len(arr)
    return arr[n:]+arr[:n]
```

# 2d rotate
## clock-wise
```python
# 2d array board
list(map(list,zip(*reversed(board))))
```

```python
[col[::-1] for col in map(list,zip(*board))]
```

## counter-clock-wise
```python
list(map(list,zip(*board)))[::-1]
```

## 특정 영역 clock wise rotate

```python
_dir_ = ((0,1),(1,0),(0,-1),(-1,0)) # 동,남,서,북
# start(sy,sx) end(ey,ex)
def rotate(sy,ey,sx,ex):
    global arr
    new_arr = [row[:] for row in arr]
    nums = (ey-sy)//2+1 #회전 횟수
    for n in range(nums)[::-1]:
        side_num = 2*n
        for dy,dx in _dir:
            for _ in range(side_num):
                ny,nx = sy+dy,sx+dx
                new_arr[ny][nx]= arr[sy][sx]
                sy,sx = ny,nx
            sy+=1
            sx+=1
    arr = [row[:] for row in new_arr]
 
```

## 2d array N-time row rotate
```python
def clock(arr,ty,n):
    global N,M
    n %= M
    for y in range(N):
        if (y+1)%ty == 0:
            arr[y] = arr[y][M-n:]+arr[y][:M-n]

def counter_clock(arr,ty,n):
    global N, M
    n %= M
    for y in range(N):
        if (y+1)%ty == 0:
            arr[y] = arr[y][n:]+arr[y][:n]

# main()
board = None
N = M = 0
with open('tmp.txt','r') as f:
    N,M = map(int,f.readline().split())
    board = [list(map(int,f.readline().split())) for _ in range(N)]
```