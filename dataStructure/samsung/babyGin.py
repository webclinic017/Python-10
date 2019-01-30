# permutation returns [[1,2,3...],[],[]]
def babyGin(num):
    for i in permutation(num):
        stat=[False]*2
        for ind,j in enumerate([i[:3],i[3:]]):
            # triple check
            if (j[0]<j[1] and j[1]<j[2])or (j[0]==j[1] and j[1]==j[2]): stat[ind]=True
            else: break
        if all(stat): return True
    return False

num = list(map(int,input().split()))
print("Yes") if babyGin(num) else print("No")
