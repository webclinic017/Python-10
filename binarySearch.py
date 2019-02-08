def binarySearch(sortedLi,x):
    # index so len-1
    l=0;r=len(sortedLi)-1
    while not l>r:
        # indexing only m; indexoutofbound cannot appear bc l>r is base cond
        m = (l+r)//2
        if sortedLi[m]==x:return m
        elif sortedLi[m]>x:r=m-1
        else:l=m+1
    return -1
li = [0,1,2,3,4,5,6,7,8,9]
print(binarySearch(li,-1))
