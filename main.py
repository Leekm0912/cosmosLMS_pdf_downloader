from urllib.request import urlretrieve
from urllib.parse import quote_plus
from bs4 import BeautifulSoup
from selenium import webdriver
import os
import configparser

from time import sleep

# ini파일 읽어오기
cf = configparser.ConfigParser()
cf.read("config.ini", encoding="utf-8")
chrome_driver_path = cf['DEFAULT']['CHROME_DRIVER_PATH']
save_path = cf['DEFAULT']['SAVE_PATH']

# 검색할 url 조합
with open("download_list", "r") as r:
    url = r.readlines()

print(url)

# 셀레니움 시작
driver = webdriver.Chrome(chrome_driver_path)
driver.get(url[0])
driver.implicitly_wait(10)
sleep(3)
driver.switch_to.frame("docFrame")
sleep(3)
# 파싱 시작
html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')
with open("save.html", "w", encoding="utf-8") as w:
    w.write(html)

# 저장 경로 설정
title = soup.select_one(".fnm").text
print(title)
dir_path = save_path + "/" + title

if not os.path.exists(dir_path):
    os.makedirs(dir_path)

# 이미지 경로를 저장할 리스트
img_list = []

for i in range(1000):
    try:
        thumb_id = soup.select_one("#thumb" + str(i)).attrs["id"]
        print(thumb_id)
        # 썸네일을 눌러야 이미지가 로딩되는 형식이라 썸네일을 하나하나 눌러줌.
        driver.find_element_by_id(thumb_id).click()
        sleep(1)
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        # 이미지가 들어있는 div 파싱
        page = soup.select_one("#page" + str(i))
        print("https://doc.coursemos.co.kr" + page.attrs["src"])
        img_list.append("https://doc.coursemos.co.kr" + page.attrs["src"])
    except AttributeError as e:
        # 오류가 났다는건 더 이상 불러올 이미지가 없다는 뜻.
        break

# 파싱 결과 확인
print(img_list)

# 이미지파일 저장
for i in range(len(img_list)):
    urlretrieve(img_list[i], f"downloads/{title}/{title}_{i}.jpg")
    print(str(i) + "번 이미지 다운로드중")

# 이미지파일 경로 백업
with open(f"downloads/{title}/image_url.txt", "w") as w:
    w.write(str(img_list))

# 드라이버 해제
driver.close()
