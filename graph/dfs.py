# adj: {'A':('B','C','D'...),'B':(),'C':(),'':(),'':(),'':()}
# visited,stack = (start,),[start]; visited를 set으로 하여 차집합 구하기 용이하게 한다.
# error: visited를 set으로 구현하면 order 순서대로 만들수가 없다.
# stack이 empty일때까지, push, visited,pop 순서로 진행
# push: 갈곳이 있을경우 adjacency push;adjacency[stack[-1]] 차집합 visited 가 존재할경우
# visited: 그냥 넣어도 됨.
# pop: push의 else일경우
def dfs(start,adj):
    visited,stack = (start,),[start]
    while stack:
        # 알파벳 순서대로 node를 방문한다고 하였을경우를 대비하여 sort시킨다.
        # >>> sorted(list({})) -> [] set이 비어있어도 error발생하지 않는다.
        diffSet=sorted(list(set(adj[stack[-1]])-set(visited)))
        if diffSet: stack.append(diffSet[0]);visited+=(diffSet[0],) # tuple에 append하기 위해서는 +=튜플 형식으로 주어야한다.
        else: stack.pop()
    print(visited)


# (4) -> int type, (4,)-> tuple type, () -> tuple type
# adj의 key에는 모든 node들이 존재해야 한다. ex) 4의 경우 node가 없지만, 4:()형식으로 주어짐.
adj = {1:(2,3,4),2:(4,),3:(4,),4:()}
dfs(1,adj)
