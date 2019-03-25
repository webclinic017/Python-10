# 주석 처리됨
import urllib.request
from selenium import webdriver
from selenium.webdriver.common.keys import Keys 
import time,csv
from selenium.webdriver.support.ui import WebDriverWait

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--incognito")
browser = webdriver.Chrome('/home/minkj1992/code/facial_project/chromedriver',chrome_options=chrome_options)
browser.implicitly_wait(1.5)

# 원하는 카테고리 설정
cat=['top','outer','bottom']
#  카테고리에 해당하는 무신사 url
num=['001','002','003']

def download_img(img,category,cnt,ext):
    path = './'+category+'/'+cnt+'.'+str(ext)
    # urlretrieve: url에서 파일을 저장하기 위해서 사용하는 urllib의 매서드
    # urllib.request.urlretrieve(image_url, 로컬에 저장할 위치)
    urllib.request.urlretrieve(img,path)

# 무신사 사이트에 들어가면 페이지 전체를 로딩하기 위해서는 시간이 걸리기에 pause_time을 설정해준다.
# 또한 scroll action을 할때도, 거기에 따라서 load를 받아야 하니 pause time을 넣어준다.
SCROLL_PAUSE_TIME=0.1  
url = 'https://store.musinsa.com/app/items/lists/'

for c,j in zip(cat,num):
    # 원하는 카테고리로 url을 쏴준다
    browser.get(url+j)
    # 셀레늄 window를 최대화 시켜서 킨다.
    browser.maximize_window()
    # 현재 저장하는 파일이 몇번째 인지 가지고 있는 변수( 파일이름 중첩 방지, ex_ 001.png 002.png )
    cur_num = 0
        
    #  만약 사진 외에도 가격 브랜드 등을 가져오고 싶으면 주석 풀면 됨
    # save to csv
    #     title_li=[]
    #     price_li=[]
    #     like_li=[]
    #     ids = []
    #  무신사는 제품들이 page화 되어 있기에 어디어디 페이지를 가져올지 지정
    for page in range(4,12):
        # 화면 이동 사이즈 (스크롤)
        target = 1000;
        # 스크롤 pause
        time.sleep(3)
        # window의 맨 밑으로 scroll 되기 전까지 target을 이동시킨다.
        while True:
            now_height = browser.execute_script("return window.pageYOffset;")
            browser.execute_script("window.scrollTo(0,{});".format(target))
            time.sleep(SCROLL_PAUSE_TIME)
            target+=1000
            new_height = browser.execute_script("return window.pageYOffset;")
            # 현재 위치가 더이상 갈곳이 없다면 값이 같게 되며, break 처리된다.
            if now_height==new_height:break
        # 스크롤을 완료하면 모든 제품들이 load되는데, items로 가져온다.
        items = browser.find_element_by_id('searchList')
        # items에서 images tag를 가져온다
        images = items.find_elements_by_css_selector('div.li_inner > div.list_img > a > img[src]')
        # images tag 정보중 src를 가져온다.
        image_urls=[]
        
        for image in images:
            # images tag 정보중 src를 가져온다.
            image_urls.append(image.get_attribute("src"))
        # 만약 csv로 따로 저장하지 않으려면, cnt_브랜드명_가격.jpg 이런식으로 img를 저장시킨다.
        for idx,image_url in enumerate(image_urls):
            ext = image_url.split('.')[-1]
            if ext in ['jpg','png','jpeg','JPG','JPEG','PNG']:
                item = items.find_element_by_css_selector('#searchList > li:nth-child('+str(idx+1)+') > div.li_inner > div.article_info')
                title = item.find_element_by_css_selector('p.item_title > a')
                try:
                    price = item.find_element_by_class_name('price')
                    price=price.text.split()[-1][:-1].replace(',','')
                except:
                    price = '0'
                try:
                    like = item.find_element_by_class_name('txt_cnt_like')
                    like = like.text.replace(',','')
                except:
                    like = '0'
                title=title.text
                # save to csv
#                 download_img(image_url,c,cur_num+idx,ext)
                file_name=str(cur_num+idx)+'_'+title+'_'+price+'_'+like
                download_img(image_url,c,file_name,ext)  
            else:
                print("error made")
        cur_num+=len(image_urls)
        # 다음(페이지)으로 가기 버튼 클릭
        button = browser.find_element_by_xpath('//*[@id="contentsItem_list"]/div[2]/div[5]/div/div/a['+str(page)+']')
        button.send_keys(Keys.ENTER)


    # save to csv
#     tmp = numpy.asarray([*zip(ids,title_li,price_li,like_li)])
#     with open('./'+c+'/'+c+'.csv', 'w', encoding='utf-16') as file:
#         writer = csv.writer(file, delimiter=',')
#         writer.writerow(fieldnames)
#         for i,t,p,l in zip(ids,title_li,price_li,like_li):
#             writer.writerow([i,t,p,l])
