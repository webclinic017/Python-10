# import
from bs4 import BeautifulSoup
from urllib.request import urlopen
 
url = urlopen("https://movie.naver.com/movie/running/current.nhn")
bs = BeautifulSoup(url, 'html.parser')
body = bs.body
 
target = body.find(class_="lst_detail_t1")
list = target.find_all('li')
no = 1
for n in range(0, len(list)) :
    print("=================================")
    print("No.",no)
    no += 1
    # 영화 제목
    title = list[n].find(class_="tit").find("a").text.strip()
    print("영화 제목 :\t", title)
    score = list[n].find(class_="star").find(class_="star_t1").find("a").find(class_='num').text.strip()
    print("영화 평점 :\t", score)
    
    # 개봉일/ 장르/ runtime
    try:
        # ['액션, SF', '181분', '2019.04.24 개봉']
        value = list[n].find(class_="info_txt1").find_all("dd")[0].text.replace("\n",'').replace("\t", "").replace('\r','').split('|')
        genre = [i.strip() for i in value[0].split(',')]
        print("영화 장르 :\t", genre)
        length = int(value[1][:-1])
        print("영화 길이 :\t", length)
        date = value[2].split()[0]
        print("영화 개봉일:\t", date)
    except IndexError:
        print("제작 장르|길이|개봉일 :\t 정보 없음")
    
    # 감독
    try:
        director = list[n].find(class_="info_txt1").find_all("dd")[1].find("span").find_all("a")
        directorList = [director.text.strip() for director in director]
        print("제작 감독 :\t", directorList)
        break
    except IndexError:
        print("제작 감독 :\t 정보 없음")
    # 출연 배우
    try:
        cast = list[n].find(class_="lst_dsc").find("dl", class_="info_txt1").find_all("dd")[2].find(class_="link_txt").find_all("a")
        castList = [cast.text.strip() for cast in cast]
        print("출연 배우 :\t", castList)
    except IndexError:
        print("출연 배우 :\t 정보 없음")
