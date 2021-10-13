# cosmosLMS_pdf_downloader
cosmos LMS에 올라와있는 pdf 이미지를 자동으로 다운로드 받아주는 도구.

# 사용법

## ✓ 크롬 버젼에 맞는 드라이버를 다운로드

### 버젼확인방법

우측상단 ... 클릭 -> 도움말 -> Chrome정보

### 크롬 드라이버 다운로드
[https://sites.google.com/a/chromium.org/chromedriver/downloads](https://sites.google.com/a/chromium.org/chromedriver/downloads)

## ✓ download_list 파일 작성

download_list 라는 파일을 작성 해 다운로드할 주소를 입력.

여러개 입력시 줄 바꿈으로 구분.

이후 경로를 config.ini에 설정

## ✓ config.ini 파일 설정

config.ini 파일을 열어 파라미터를 수정해 사용. (주석 참고)

```
[DEFAULT]
# 이미지파일 저장 경로 (마지막 / 제외하고)
# ex)./downloads
SAVE_PATH = ./downloads

# 크롬 드라이버 경로 설정(마지막 / 제외하고)
# ex) ./chromedriver_win32_v87
CHROME_DRIVER_PATH = ./chromedriver

# 크롤링 할 url 리스트
# 여러개 입력시 줄바꿈으로 구분
DOWNLOAD_LIST = ./download_list
```

---

# 라이브러리 다운로드 필요

## **Standard Library**

- configparser
    
    ⇒소스와 설정파일 분리를 위해 사용.
    
- os
    
    ⇒ os 명령어 실행.
    
- time
    
    ⇒ sleep 기능을 위해 사용.
    

## **3rd party Library**

- urllib
    
    ⇒ 이미지 다운로드를 위해 사용
    
- bs4
    
    ⇒ html 요소 파싱을 위해 사용
    
- selenium
    
    ⇒ 웹 자동화 관련 라이브러리
    
- img2pdf

    ⇒ 다운로드 받은 이미지를 pdf 파일로 변환시 사용.
    

## 한번에 설치 → `pip3 install -r requirements.txt`

---
