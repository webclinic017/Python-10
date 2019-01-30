def permutation(li):
    # base
    if len(li)<=1:
        print(type(li))
        return li
    res = []
    # 끝에것 뺀 나머지, 1개일경우에는 어차피 permutation 1개이므로
    for i in range(len(li)):
        ele = [li[i]]
        rmLi = li[:i]+li[i+1:]
        for p in permutation(rmLi):
            pass
            # res.append(ele+p)
    return res
print(*permutation([1,2,3]))
