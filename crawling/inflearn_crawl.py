from urllib.request import urlopen
from bs4 import BeautifulSoup
import requests
# from collections import namedtuple

def encoding(language,parser):
    pass

url = "https://www.inflearn.com/course/%EC%9B%B9-mvc/dashboard"
resp = requests.get(url)
resp.raise_for_status()
resp.encoding = 'utf-8'
html = resp.content
soup = BeautifulSoup(html, "html.parser")

# html = urlopen(url).read().decode('euc-kr')
soup = BeautifulSoup(html, "html.parser",from_encoding='utf-8')
curriculum = soup.find("div",class_="curriculum_accordion unit_section_list")

print(curriculum)


# 강의 섹션, 강의, 강의에 따른 이름과 시간을 named tuple에 저장합니다.
# {
#     "1": [
#             ("lec_name","lec_time"),

#             ]
# }


Sections = {}