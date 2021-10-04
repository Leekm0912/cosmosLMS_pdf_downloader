from urllib.request import urlretrieve
from urllib.parse import quote_plus
from bs4 import BeautifulSoup
from selenium import webdriver
import os
import configparser

from time import sleep

# ini파일 읽어오기
cf = configparser.ConfigParser()
cf.read("config.ini",encoding="utf-8")
search = cf['DEFAULT']['SEARCH']
chrome_driver_path = cf['DEFAULT']['CHROME_DRIVER_PATH']
img_class_name =  cf['DEFAULT']['GOOGLE_IMG_CLASSNAME']
save_path =  cf['DEFAULT']['SAVA_PATH']

# 검색할 url 조합
with open("download_list", "r") as r:
    url = r.readlines()

with open("copy.html", "r") as r:
    html_read = r.read()

print(url)

# 셀레니움 시작
#driver = webdriver.Chrome(chrome_driver_path)
#driver.get(url[0])
#driver.implicitly_wait(10)
#driver.switch_to.frame("docFrame")
# 파싱 시작
#html = driver.page_source
soup = BeautifulSoup(html_read, 'html.parser')

#img = soup.find("#contents")
#print(soup)

for i in range(20):
    try:
        img = soup.select_one("#page" + str(i))
        print(img.attrs["src"])
    except AttributeError as e:
        print(e)

'''
# 구글의 이미지 태그 대입
img = soup.select(img_class_name)
# 파싱 결과 확인
print(img)

# url을 담을 리스트
imgurl = []

# 반복문 돌면서 이미지의 src 추출
# 이미지 경로가 src 또는 data-src로 되어있음
for i in img:
    try:
        imgurl.append(i.attrs["src"])
    except KeyError:
        imgurl.append(i.attrs["data-src"])

print("검색된 이미지 개수 :",len(imgurl))

# 저장 경로 설정
dir_path = save_path + "/" + search

if not os.path.exists(dir_path):
    os.makedirs(dir_path)

# 다운받은 사진 url을 담은 txt파일과, 이미지파일 저장
with open(dir_path + "/ImageURL_"+search+".txt","a") as a:
    n=1
    # imgurl 리스트에 든 이미지들 다운받아줌
    for i in imgurl:
        try:
            urlretrieve(i,"downloads/"+search+"/"+search+str(n)+".jpg")
            print(str(n)+"번 이미지 다운로드중")
            a.write(str(n)+"번사진:"+i+"\n")
            n += 1
        except:
            print(n,"번 이미지 다운로드중 오류 발생. 건너뜁니다")
# 드라이버 해제
driver.close()'''