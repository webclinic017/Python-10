- 190209 멋사 스터디를 통해서 배운 것들
- 친구들 windows, env 환경에서 가상환경을 키는 것이 까다롭다. venv workon하는 방법 정리해서 설명해주는게 좋겠다.
- [참고자료](https://yamalab.tistory.com/64)

# 1. Get 방식
- `bs4`
- 
- 아래 예제는 벅스 실시간 순위 크롤링 해와서 csv로 저장 한 뒤, 다시 읽어 오는 코드이다.
```python
import requests
from bs4 import BeautifulSoup
import re
# 1. 원하는 url에게 get 방식으로 요청을 한다.
req = requests.get('https://music.bugs.co.kr/chart')
# 2. request에서 필요한 content데이터만 가져온다.
html = req.content
# 3. binary 형식을 html형식으로 바꿔준다.
soup = BeautifulSoup(html, 'lxml') # pip install lxml
# 4-1. soup 데이터에서 p tag에 title class 데이터만 find 하여 긁어 온다.
list_song = soup.find_all(name="p", attrs={"class":"title"})
# 4-2. 마찬가지로 soup 데이터에서 p tag에 artist class 데이터만 find 하여 긁어 온다.
list_artist = soup.find_all(name="p", attrs={"class":"artist"})

# 곡명 추출
# list_song은 여러개의 곡들이 존재하기 때문에, for문을 돌면서 각 노래들의 title text 데이터를 가져온다.
for index in range(0, len(list_song)):
    title = list_song[index].find('a').text
    print(index+1, ' : ', title)
    # 100개를 넘어 가면 break를 하여 코드를 중지시켜준다. (무한 루프 방지)
    if index == 100:
        break

# 피처링 제거
# 피쳐링을 사이트를 보면 (feat. 민욱)처러 '('으로 시작하는데
# .split("(")= (으로 시작하는 부분에서 split해라
# 이렇게 split하면 [신청곡 (Feat. SUGA of BTS)] -> [신청곡, Feat. SUGA of BTS]으로 나눠진다.
# [신청곡, Feat. SUGA of BTS] 데이터에서 [0]번째 데이터를 가져오면 곡 명이 빠져나오게 된다.
for index in range(0, len(list_song)):
    title = list_song[index].find('a').text
    print(index+1, ' : ', title.split("(")[0])
    if index == 100:
        break

# csv로 저장
import csv
# with open 을 사용하여 file을 열어준다( 만약 파일을 빼내기 위해서는 with open을 사용하면 된다.)
# 'melon_chart.csv'라는 이름의 excel 파일을 생성해준뒤 열어준다.
# 열리 excel파일에 writerow()를 사용하여 칼럼 명을 ['rank', 'song', 'artist'] 로 지정해준다.
with open('melon_chart.csv', 'w', encoding='utf-8') as file:
    writer = csv.writer(file, delimiter=',')
    writer.writerow(['rank', 'song', 'artist'])
    # for문을 돌면서 100개의 데이터를 저장한다.
    for index in range(0, len(list_song)):
        title = list_song[index].find('a').text
        artist = list_artist[index].find('a').text
        writer.writerow([index+1, title, artist])
        if index == 100:
            break

# 만약 csv로 저장한 데이터를 다시 읽어 들이고 싶다면, pandas 라이브러리를 사용하여 excel 파일을 열어주어 datas변수에 데이터들을 읽어 올 수 있다.
# 저장된 파일 pd로 읽기
import pandas as pd
datas = pd.read_csv('melon_chart.csv')
```

## 문제점
- 네이버 실시간, 멜론실시간 차트 같은 경우에 robot.txt가 되어있어서 requset해서 html로 받을 수가 없었다.
- 삽질하다 selenium을 사용하니 바로 해결

        <meta content="네이버 :: 서비스에 접속할 수 없습니다." lang="ko" name="description"/><title>[접근 오류] 서비스에 접속할 수 없습니다.</title>

# 2. Post 방식
- 만약 사이트가 post 방식으로 form이 생성 되었다면, post를 사용하여 데이터를 가져와야한다.
- [메인 참고자료](https://rednooby.tistory.com/97)
- [참고자료](https://diary.virlit.com/9)
- [참고자료2](https://beomi.github.io/2017/01/20/HowToMakeWebCrawler-With-Login/)
특정 URL의 웹 페이지는 POST 방식으로 데이터를 얻어와야 한다.

python의 request 패키지를 이용하여 헤더에 추가적인 정보를 붙이고, post 방식으로 데이터를 가져올 수 있다.

아래의 예제는 네이버 API 중, 음성합성 API를 POST 방식으로 가져오는 예제이다. 

엄밀히 말하자면 웹 크롤링은 아니지만, HTTP 통신에 데이터를 추가하여 POST 방식으로 데이터를 얻어오는 예제이다.

이 코드를 돌려보려면 개발자 아이디로 가입하여 API 인증을 완료해야 한다.

```python
import os
import sys
import urllib.request

client_id = "Your Client_ID" # Client_ID 입력
client_secret = "Your_Client_Password" # Client_Password 입력

encText = urllib.parse.quote("원하는 음성 내용 입력.")
data = "speaker=mijin&speed=0&text=" + encText;

url = "https://openapi.naver.com/v1/voice/tts.bin"
request = urllib.request.Request(url)
request.add_header("X-Naver-Client-Id", client_id)
request.add_header("X-Naver-Client-Secret", client_secret)
response = urllib.request.urlopen(request, data=data.encode('utf-8'))
rescode = response.getcode()

if(rescode==200):
    print("TTS mp3 저장")
    response_body = response.read()
    with open('fastcampus.mp3', 'wb') as f:
        f.write(response_body)
else:
    print("Error Code:" + rescode)
```

# 3. 동적 방식
- `selenium`을 사용하면 robot.txt같은 문제를 해결해줄 수 있다.

```python
from selenium import webdriver
from bs4 import BeautifulSoup
# 드라이버 위치 
browser = webdriver.Chrome('/home/minkj1992/code/facial_project/chromedriver')
browser.implicitly_wait(3)
# 원하는 site
browser.get('https://www.melon.com/chart/')
html = browser.page_source
# 소스를 html화 시켜준다.
soup = BeautifulSoup(html, 'html.parser')

# 개발자 도구에서 copy selector
datas = soup.select('#frm > div > table > tbody > tr:nth-child(1) > td:nth-child(6) > div > div')

```

# 4. `selenium`을 활용하여 이미지 크롤링하기
```python
import urllib.request
import random
from selenium import webdriver
from bs4 import BeautifulSoup
import re
class AppURLopener(urllib.request.FancyURLopener):
    version = "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.69 Safari/537.36"
urllib._urlopener = AppURLopener()
def download_img(datas,cnt):
    full_name = "./images/"+"athlete_"+str(cnt)+".png"
    urllib._urlopener.retrieve(str(datas),full_name)


browser = webdriver.Chrome('/home/minkj1992/code/facial_project/chromedriver')
browser.implicitly_wait(3)
url = "https://asiangames2018.id/athletes/detail/"
for cnt,j in enumerate(random.sample(range(1,1000),300)):
    try:
        browser.get(url+str(j))
        html = browser.page_source
        soup = BeautifulSoup(html, 'html.parser')
        # select_one 쓰는게 핵심
        datas = soup.select_one('body > div.sports-detail-wrapper > div.container-sport-detail.col-xs-12 > div.container-sport-detail-flag-desc.col-xs-8.col-xs-offset-2 > div.left.col-md-6 > div > img[src]')
        download_img(datas['src'],cnt)
    except:
        # 사진이 없을 경우 또는 id 가 없을 경우
        print("pass happend!")
        pass
```


