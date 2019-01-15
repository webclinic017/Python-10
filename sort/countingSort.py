def countingSort(li):
    max_v=max(li)
    
    out_li = [0]*len(li)
    # max value +1 크기의 count_li
    count_li = [0]*(max_v+1)

    # count occurence
    for i in li:
        count_li[i] += 1

    # Update(partial_sum count_li)
    for i in range(max_v):
        count_li[i+1] +=count_li[i]

    for i in li[::-1]:
        out_li[count_li[i]-1] = i
        count_li[i] -= 1
    return out_li

li = []
for _ in range(int(input())):
    li.append(int(input()))

print(*countingSort(li),sep="\n")


# second try
# TIL: f=open(0)이 아직 무슨뜻인지는 모르겠는데, 0에 input데이터가 존재하는 것 같다.
# max_value+1 배열 한개를 만들고, partial_sum없이 input받을때마다 숫자 index에다가 1씩 더한다.
# 이후 value만큼 반복하면서 print index를 찍어준다. 참고로 배열은 +1해준이유는 index와 숫자간의 차이를 없애주기 위해서이다.

n=10001;a=[0]*n;f=open(0);f.readline()
for i in f:a[int(i)]+=1
for i in range(n):print("%s\n"%i*a[i],end="")
