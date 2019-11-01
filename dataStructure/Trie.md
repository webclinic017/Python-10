# Trie
> https://blog.ilkyu.kr/entry/%ED%8C%8C%EC%9D%B4%EC%8D%AC%EC%97%90%EC%84%9C-Trie-%ED%8A%B8%EB%9D%BC%EC%9D%B4-%EA%B5%AC%ED%98%84%ED%95%98%EA%B8%B0

- 자동 완성에 사용
- 컴퓨터에서 검색을 뜻하는 `retrieval`에서 따온 단어
- Prefix tree라고도 함
- 검색 시간 복잡도 `O(m)` (m = 문자열최대 길이)


## 구현

- `Node 자료구조 뼈대`

```python
'''
key = 알파벳 하나 (char)
data
    = 끝 글자 여부 ( string )
    = 만약 끝글자가 아니라면 None
    = John과 Johnson이 존재할 경우, John이 끝글자라는 것은 data를 통해서 None이 아니라면 으로 판단
    = 위의 상황 때문에, children == {}과 같은 방법으로 끝글자를 판단하지 못함.
children = children Node를 담고있는 dict (dictionary)
'''

class Node:
    def __init__(self, key, data=None):
        self.key = key
        self.data = data
        self.children = {}
```


- `Trie 자료구조 뼈대`

```python

class Trie:
    def __init__(self):
        self.head = Node(None)

    '''
    트라이에 문자열을 삽입
    '''
    def insert(self,string):
        pass

    '''
    트라이에 주어진 단어 string이 존재하는지 여부 return
    '''
    def search(self,string):
        pass

    '''
    주어진 prefix로 시작하는 단어들을 트라이에서 찾아 리스트 형태로 반환
    '''
    def starts_with(self,prefix):
        pass
```


- `insert(string)`
```python
    def insert(self,string):
        cur_node = self.head

        for char in string:
            if char not in cur_node.children:
                cur_node.children[char] = Node(char)
            cur_node = cur_node.children[char]

        else:
            # 마지막 node에 string 저장
            cur_node.data = string
```

- `search(string)`
```python
    def search(self,string):
        cur_node = self.head

        for char in string:
            # children이 {}일 경우 포함 검색
            if char in cur_node.children:
                cur_node = cur_node.children[char]
            else:
                return False
        else:
            if cur_node.data != None:
                return True
```

- `start_with(prefix)`
```python
    from collections import deque

    def starts_with(self,prefix):
        cur_node = self.head
        result = []
        sub_trie = None

        for char in prefix:
            if char in cur_node.children:
                cur_node = cur_node.children[char]
            else:
                return None
        else:
            sub_trie = cur_node

        queue = deque(sub_trie.children.values())

        while queue:
            cur = queue.popleft()
            if cur.data != None:
                result.append(cur.data)
            queue.extend(cur.children.values())

        return result

```


- `전체 소스코드`
```python
from collections import deque

class Node:
    def __init__(self, key, data=None):
        self.key = key
        self.data = data
        self.children = {}


class Trie:
    def __init__(self):
        self.head = Node(None)

    '''
    트라이에 문자열을 삽입
    '''
    def insert(self,string):
        cur_node = self.head

        for char in string:
            if char not in cur_node.children:
                cur_node.children[char] = Node(char)
            cur_node = cur_node.children[char]

        else:
            # 마지막 node에 string 저장
            cur_node.data = string


    '''
    트라이에 주어진 단어 string이 존재하는지 여부 return
    '''
    def search(self,string):
        cur_node = self.head

        for char in string:
            # children이 {}일 경우 포함 검색
            if char in cur_node.children:
                cur_node = cur_node.children[char]
            else:
                return False
        else:
            if cur_node.data != None:
                return True

    '''
    주어진 prefix로 시작하는 단어들을 트라이에서 찾아 리스트 형태로 반환
    '''
    
    def starts_with(self,prefix):
        cur_node = self.head
        result = []


        for char in prefix:
            if char in cur_node.children:
                cur_node = cur_node.children[char]
            else:
                return None
        
        sub_trie = cur_node
        queue = deque(sub_trie.children.values())

        while queue:
            cur = queue.popleft()
            if cur.data != None:
                result.append(cur.data)
            queue.extend(cur.children.values())

        return result
```

## 응용 문제
- [카카오 2019 동계 기출](https://programmers.co.kr/learn/courses/30/lessons/60060)
