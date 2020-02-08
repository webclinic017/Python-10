# LIS

- [About LIS](https://shoark7.github.io/programming/algorithm/3-LIS-algorithms)

- [최대 연속 부분수열 합/`Largest sum of continuous subarray in a non-empty array`](https://shoark7.github.io/programming/algorithm/4-ways-to-get-subarray-consecutive-sum)

```
- LIS with value
    - Largest sum of continuous subarray in a non-empty array
- LIS with length
    - 증감수열
```

## Largest sum of continuous subarray in a non-empty array

- `O(n^2)`
- `O(nlogn)`
```
- [lo, mid], 즉 원 배열의 왼쪽 반에 있을 경우
- [mid+1, hi], 원 배열의 오른쪽 반에 있을 경우
- [그 외], 양쪽 절반에 걸쳐 있는 경우
```
```python
def divide_conquer(arr):
    N = len(arr)

    def find(lo, hi):
        # 1.
        if lo == hi:
            return arr[lo]

        mid = (lo + hi) // 2
	# 2.
        left = find(lo, mid)
        right = find(mid+1, hi)

        # 3.
        tmp = 0
        left_part = MIN
        for i in range(mid, lo-1, -1):
            tmp += arr[i]
            left_part = max(left_part, tmp)

        tmp = 0
        right_part = MIN
        for i in range(mid+1, hi+1):
            tmp += arr[i]
            right_part = max(right_part, tmp)

        # 4.
        return max(left, right, left_part + right_part)

    # 5.
    return find(0, N-1)
```
- `O(n)`
```python
def dynamic_programming(arr):
    cache = [None] * len(arr)
    # 1.
    cache[0] = arr[0]

    # 2.
    for i in range(1, len(arr)):
        cache[i] = max(0, cache[i-1]) + arr[i]

    return max(cache)
```

