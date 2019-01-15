#first try
#TIL: insertioin sort를 활용하여 insert 될때마다 
#TIL: reversed(s) == s[::-1]
#TIL: print(*list,sep='\n')
#TIL: s.insert(index,value)

s = []
for _ in range(int(input())):
  if len(s)==0:
    s.append(int(input()))
  else:
  #맨 뒤에서 부터 index를 빼주면서 전진한다.
    ins,indx = int(input()),len(s)
    for i in s[::-1]:
      if ins>=i:
        break
      indx-=1
    s.insert(indx,ins)
print(*s,sep='\n')
