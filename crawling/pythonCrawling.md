- 190209 멋사 스터디를 통해서 배운 것들
- 친구들 windows, env 환경에서 가상환경을 키는 것이 까다롭다. venv workon하는 방법 정리해서 설명해주는게 좋겠다.
- [참고자료](https://yamalab.tistory.com/64)

# 1. Get 방식
- `bs4`
- 아래 예제는 벅스 실시간 순위 크롤링 해와서 csv로 저장 한 뒤, 다시 읽어 오는 코드이다.
```python
import requests
from bs4 import BeautifulSoup
import re

req = requests.get('https://music.bugs.co.kr/chart')
html = req.content
soup = BeautifulSoup(html, 'lxml') # pip install lxml
list_song = soup.find_all(name="p", attrs={"class":"title"})
list_artist = soup.find_all(name="p", attrs={"class":"artist"})

# 곡명 추출
for index in range(0, len(list_song)):
    title = list_song[index].find('a').text
    print(index+1, ' : ', title)
    if index == 100:
        break

# 피처링 제거
for index in range(0, len(list_song)):
    title = list_song[index].find('a').text
    print(index+1, ' : ', title.split("(")[0])
    if index == 100:
        break

# csv로 저장
import csv

with open('melon_chart.csv', 'w', encoding='utf-8') as file:
    writer = csv.writer(file, delimiter=',')
    writer.writerow(['rank', 'song', 'artist'])
    for index in range(0, len(list_song)):
        title = list_song[index].find('a').text
        artist = list_artist[index].find('a').text
        writer.writerow([index+1, title, artist])
        if index == 100:
            break

# 저장된 파일 pd로 읽기
import pandas as pd
datas = pd.read_csv('melon_chart.csv')
```

## 문제점
- 네이버 실시간, 멜론실시간 차트 같은 경우에 robot.txt가 되어있어서 requset해서 html로 받을 수가 없었다.
- 삽질하다 selenium을 사용하니 바로 해결

        <meta content="네이버 :: 서비스에 접속할 수 없습니다." lang="ko" name="description"/><title>[접근 오류] 서비스에 접속할 수 없습니다.</title>

# 2. Post 방식
- `request`
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
- `selenium`

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



