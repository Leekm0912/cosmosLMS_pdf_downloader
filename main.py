from time import sleep
import os
import configparser

from urllib.request import urlretrieve
from bs4 import BeautifulSoup
from selenium import webdriver
import img2pdf


def makePDF(src_dir, data_path=None):
    if not data_path:
        data_path = []
        path = f"./downloads/{src_dir}"
        for file in os.listdir(path):
            if file.endswith(".png"):
                data_path.append(file)
        data_path.sort(key=lambda x: int(x.split("_")[1].split(".")[0]))
        print("data_path", data_path)

    load_image = []
    for img in data_path:
        with open(f"{path}/{img}", 'rb') as f:
            load_image.append(f.read())

    with open(f"downloads/{src_dir}/{src_dir}.pdf", "wb") as pdf_file:
        pdf_file.write(img2pdf.convert(load_image))


# ini 파일 읽어오기
cf = configparser.ConfigParser()
cf.read("config.ini", encoding="utf-8")
chrome_driver_path = cf['DEFAULT']['CHROME_DRIVER_PATH']
save_path = cf['DEFAULT']['SAVE_PATH']

# 검색할 url 불러오기
with open("download_list", "r") as r:
    url_list = r.readlines()

print(url_list)

for url in url_list:
    # 셀레니움 시작
    driver = webdriver.Chrome(chrome_driver_path)
    driver.get(url.strip("\n"))
    driver.implicitly_wait(10)
    sleep(3)
    # 이미지가 frame안에 들어있어서 switch_to_frame으로 프레임 안으로 이동
    driver.switch_to.frame("docFrame")
    sleep(3)
    # 파싱 시작
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    with open("save.html", "w", encoding="utf-8") as w:
        w.write(html)

    # 저장 경로 설정
    # pdf 문서의 제목 파싱
    title = soup.select_one(".fnm").text
    print(title)
    dir_path = save_path + "/" + title

    # 저장 폴더가 없다면 생성해줌
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)

    # 이미지 경로를 저장할 리스트
    img_list = []

    # 이미지 파싱부분
    i = 0  # 순서 count를 위한 변수 선언
    while True:
        try:
            thumb_id = soup.select_one("#thumb" + str(i)).attrs["id"]
            # 썸네일을 눌러야 이미지가 로딩되는 형식이라 썸네일을 하나하나 눌러줌.
            driver.find_element_by_id(thumb_id).click()
            # 로딩시간 1초정도 대기
            sleep(1)
            # 이미지가 들어있는 div 파싱
            html = driver.page_source
            soup = BeautifulSoup(html, 'html.parser')
            page = soup.select_one("#page" + str(i))
            # 이미지 리스트에 추가
            print("https://doc.coursemos.co.kr" + page.attrs["src"])
            img_list.append("https://doc.coursemos.co.kr" + page.attrs["src"])
            # 작업이 끝났으면 index 1 증가
            i += 1
        except AttributeError as e:
            # 오류가 났다는건 더 이상 불러올 이미지가 없다는 뜻.
            break

    # 파싱 결과 확인
    print(img_list)

    img_save_path = []
    # 이미지파일 저장
    for i in range(len(img_list)):
        print(str(i) + "번 이미지 다운로드중")
        img_path = f"downloads/{title}/{title}_{i}.png"
        urlretrieve(img_list[i], img_path)
        img_save_path.append(img_path)

    # 이미지파일 경로 백업
    with open(f"downloads/{title}/image_url.txt", "w") as w:
        w.write(str(img_list))

    # pdf 생성
    makePDF(title)

    # 드라이버 해제
    driver.close()
