#-*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import requests
import urllib
import pandas as pd
import os
from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import time
from selenium.webdriver.common.keys import Keys
import datetime as dt

def twitterScraper():
    #firefox 브라우져 다운로드 필요
    binary=FirefoxBinary("C:/Program Files/Mozilla Firefox/firefox.exe")  
    #geckodriver.exe 다운로드 후 본인환경에 맞게 경로 수정
    browser=webdriver.Firefox(executable_path='C:/Program Files/geckodriver/geckodriver.exe',firefox_binary=binary) 
    
    print "검색어 입력"
    title = raw_input().decode("cp949").encode("utf-8")

    print "시작 연도 입력"
    year_s = int(raw_input())
    print "시작 월 입력"
    month_s = int(raw_input())
    print "시작 일 입력"
    day_s = int(raw_input())
    
    print "종료 연도 입력"
    year_e = int(raw_input())
    print "종료 월 입력"
    month_e = int(raw_input())
    print "종료 일 입력"
    day_e = int(raw_input())

    startdate=dt.date(year_s,month_s,day_s)

    untildate = startdate + dt.timedelta(days=1)

    enddate=dt.date(year_e,month_e,day_e)

    url = "https://twitter.com/search?"

    totalfreq = []
    tweetContents = []

    while not enddate==startdate:

        startdate_str=str(startdate)
        untildate_str=str(untildate)
        pre_params= title+" since:"+startdate_str+" until:"+untildate_str
        params=urllib.urlencode({"q":pre_params})
       
        url2=url+params

        browser.get(url2)
        html = browser.page_source
        soup=BeautifulSoup(html,"html.parser")

        lastHeight = browser.execute_script("return document.body.scrollHeight")
        
        wordfreq=0

        while True:
                dailyfreq={'Date':startdate}
                
                tweets=soup.find_all("p",{"class":"TweetTextSize"})
                wordfreq += len(tweets)
                for i in tweets:
                    dailytweet={}
                    dailytweet['contents']=i.text.replace(',',' ')
                    dailytweet['date']=startdate
                    
                    tweetContents.append(dailytweet)

                browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(2)  #인터넷 환경이 좋지 않을 경우, 숫자크기 크게

                newHeight = browser.execute_script("return document.body.scrollHeight")
                print newHeight

                if newHeight != lastHeight:
                    html = browser.page_source
                    soup= BeautifulSoup(html,"html.parser")
                    tweets=soup.find_all("p",{"class":"TweetTextSize"})
                    wordfreq += len(tweets)
                    for i in tweets:
                        dailytweet={}
                        dailytweet['date']=startdate
                        dailytweet['contents']=i.text
                        tweetContents.append(dailytweet)

                else:
                    dailyfreq["Frequancy"]=wordfreq
                    wordfreq=0
                    totalfreq.append(dailyfreq)
                    startdate=untildate
                    untildate+=dt.timedelta(days=1)
                    dailyfreq={}
                    break

                lastHeight=newHeight
    
    df1 = pd.DataFrame(totalfreq)
    df2 = pd.DataFrame(tweetContents)
    
    my = os.getcwd()
    
    fileName1 = title+'daily_tweets.csv'
    fileName2 = title+'tweetContents.csv'
    
    # os.getcwd에서 나온 워킹디렉터리에 Movie_twitter 폴더 작성 필요
    file1= os.path.join(my, 'Movie_twitter', fileName1) 
    file2 = os.path.join(my, 'Movie_twitter', fileName2)

    df1.to_csv(file1.decode('utf-8'), header=True, index = False, encoding='utf-8')
    df2.to_csv(file2.decode('utf-8'), header=True, index = False, encoding='utf-8')

def main():
    twitterScraper()

if __name__ == '__main__':
    main()

