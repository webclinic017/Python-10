
#단점: merge sort는 기본적으로 n크기의 메모리가 추가적으로 필요하다.
#장점: 정렬 상태와 무관하게(quick의 경우에는 worst n^2) nlogn으로 안정, n^2에 비하여(bubble, insert,selection) O(nlogn)이다.
#장점2: max mem을 넘지 않게 반반씩 잘라가면서,재귀호출로 parallel하게 작업하여 성능 향상을 꾀할 수 있다.
#first try
#TIL: mergesort = 1)divide 2)sort 3)merge
#merge sort의 관건은 새로운 배열을 최대한 만들지 않는 것이다. 
#TIL: li[piv:]=L[l:]

from sys import stdin,stdout
def mergeSort(li):
  if len(li)>1:
    mid = len(li)//2
    L,R=li[:mid],li[mid:]
    mergeSort(L);mergeSort(R)
    l=piv=r=0
    while l<len(L) and r<len(R):
      if L[l]<R[r]: li[piv]=L[l];l+=1
      else: li[piv]=R[r];r+=1
      piv+=1
    if l==len(L): li[piv:]=R[r:]
    elif r==len(R): li[piv:]=L[l:]
li=[]
for i in range(int(stdin.readline())):
  li.append(int(stdin.readline()))
mergeSort(li)
for i in li:
  stdout.write(str(i)+'\n')
