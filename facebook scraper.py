# -*- coding: utf-8 -*-
from selenium import webdriver
from bs4 import BeautifulSoup
import requests

path="D:\chromedriver_win32\chromedriver.exe"	#다운로드 된 chromdrvier.exe 경로
driver=webdriver.Chrome(path)

driver.get("https://www.facebook.com/")		#facebook페이지 접속

#login     
element_id = driver.find_element_by_id("email")
element_pw = driver.find_element_by_id("pass")
element_id.send_keys("*****")		#본인 Facebook id
element_pw.send_keys("*****")		#본인 Facebook password
driver.find_element_by_xpath("""//*[@id="loginbutton"]""").click()		#로그인 버튼 클릭

#search
search_key="신과함께"	#검색하고 싶은 키워드
search_link="https://www.facebook.com/search/str/"+search_key+"/keywords_blended_posts?filters=eyJycF9hdXRob3IiOiJ7XCJuYW1lXCI6XCJtZXJnZWRfcHVibGljX3Bvc3RzXCIsXCJhcmdzXCI6XCJcIn0ifQ%3D%3D&epa=SEE_MORE"
driver.get(search_link)

#scroll
post_list=[]
for i in range(1,100):
   driver.execute_script("window.scrollTo(0,document.body.scrollHeight);")		#페이지 스크롤 내리기
   time.sleep(1)	#1초 쉬고,

#post
html_doc=driver.page_source		#현재 페이지 소스를 가져온다.
soup=BeautifulSoup(html_doc, 'html.parser')

raw_list=soup.find_all('div','_5pbx userContent _3576')		#div태그에 class이름이 '_5pbx userContent _3576'인것을 찾는다.
print("totla number of items: ",len(raw_list))		#raw_list에 들어온 원소 수.
for raw in raw_list:
   post_list.append(raw.text)	#raw_list에 원소 중 text만 가져온다. 이를 post_list에 추가.

for p in post_list:		#post_list의 원소를 하나씩 출력한다.
   print(p,"\n")
