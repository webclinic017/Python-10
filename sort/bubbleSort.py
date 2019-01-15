# len()-1 = idx화, 만약 i+1까지 비교하지 않는다면 그냥 range(len(S))
for sorted_num in range(len(S)-1):
    # n-1번 큰 녀석들을 찾는다.
    # sorted_num = 기존에 정렬된 요소 갯수.
    # len(S)-1-sorted_num = n-1개 정렬하면 되는데, 그중에서 정렬된 요소들 삭제한 만큼 비교
    for i in range(len(S)-1-sorted_num):
        if S[i]>S[i+1]:
            #swap
            S[i],S[i+1]=S[i+1],S[i]   
